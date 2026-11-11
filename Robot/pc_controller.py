"""Run the EV3 command server over Bluetooth Classic (RFCOMM).

Install pybricks-cli, then run this file from a terminal. The script connects
using RFCOMM explicitly, uploads brick_controller.py, and passes the terminal
through so commands and telemetry are exchanged live.
"""

from __future__ import annotations

import argparse
import codecs
import queue
import shutil
import subprocess
import sys
import threading
from pathlib import Path


BRICK_PROGRAM = Path(__file__).with_name("brick_controller.py")
DEFAULT_HUB_NAME = "The Winner"


class PybricksSession:
    """Upload the EV3 controller and exchange command/output lines over RFCOMM."""

    _STOP = object()

    def __init__(self, hub_name: str = DEFAULT_HUB_NAME) -> None:
        self.hub_name = hub_name
        self.status = "disconnected"
        self.error: str | None = None
        self._commands: queue.Queue[object] = queue.Queue()
        self._messages: queue.Queue[str] = queue.Queue(maxsize=500)
        self._thread: threading.Thread | None = None
        self._finished = threading.Event()

    @property
    def connected(self) -> bool:
        return self.status.startswith("connected")

    @property
    def finished(self) -> bool:
        return self._finished.is_set()

    def start(self) -> None:
        if self._thread is not None:
            return
        self.status = "connecting"
        self._thread = threading.Thread(target=self._thread_main, name="PybricksSession", daemon=True)
        self._thread.start()

    def send_command(self, command: str) -> None:
        command = command.strip()
        if not command:
            return
        if "\n" in command or "\r" in command:
            raise ValueError("send one brick command per call")
        if self._finished.is_set():
            raise RuntimeError(self.error or "Pybricks session has stopped")
        self._commands.put(command + "\n")

    def receive_messages(self) -> list[str]:
        messages = []
        while True:
            try:
                messages.append(self._messages.get_nowait())
            except queue.Empty:
                return messages

    def close(self, timeout: float = 5.0) -> None:
        if self._thread is None:
            return
        if not self._finished.is_set():
            self._commands.put(self._STOP)
        self._thread.join(timeout)
        if self._thread.is_alive():
            self._publish_message("Connection is still shutting down.")

    def _publish_message(self, message: str) -> None:
        try:
            self._messages.put_nowait(message)
        except queue.Full:
            try:
                self._messages.get_nowait()
            except queue.Empty:
                pass
            try:
                self._messages.put_nowait(message)
            except queue.Full:
                pass

    def _thread_main(self) -> None:
        try:
            import anyio

            anyio.run(self._async_session)
        except Exception as error:
            self.error = describe_error(error)
            self.status = "error: {0}".format(self.error)
            self._publish_message("Connection error: {0}".format(self.error))
        finally:
            if self.status.startswith("connected"):
                self.status = "disconnected"
            self._finished.set()

    async def _async_session(self) -> None:
        import anyio
        import pb_client

        async with pb_client.connect() as service:
            existing_hubs, _default_hub = await service.list_hubs()
            for existing_hub in existing_hubs:
                if existing_hub.name == self.hub_name and existing_hub.transport != "rfcomm":
                    await service.disconnect_hub(existing_hub.id)

            hub = await service.connect_hub(name=self.hub_name, transport="rfcomm")
            try:
                program = await pb_client.compile_script(BRICK_PROGRAM)

                async with service.attach(hub_id=hub.id) as events:
                    async with anyio.create_task_group() as tasks:
                        tasks.start_soon(self._read_events, events)
                        await service.run_program(program, hub_id=hub.id, wait=False)
                        self.status = "connected to {0} via {1}".format(hub.name, hub.transport)
                        await service.write_stdin(b"watchdog 2500\n", hub_id=hub.id)

                        while True:
                            try:
                                command = await anyio.to_thread.run_sync(
                                    self._commands.get, True, 0.5
                                )
                            except queue.Empty:
                                await service.write_stdin(b"heartbeat\n", hub_id=hub.id)
                                continue
                            if command is self._STOP:
                                break
                            await service.write_stdin(command.encode("utf-8"), hub_id=hub.id)

                        try:
                            await service.write_stdin(b"quit\n", hub_id=hub.id)
                            await anyio.sleep(0.1)
                        except Exception:
                            pass
                        tasks.cancel_scope.cancel()
            finally:
                # Hub connections belong to the Pybricks service, not this
                # client context, so explicitly stop the program and release
                # RFCOMM on every exit path.
                with anyio.move_on_after(1):
                    try:
                        await service.stop_program(hub_id=hub.id)
                    except Exception:
                        pass
                with anyio.move_on_after(2):
                    try:
                        await service.disconnect_hub(hub.id)
                    except Exception:
                        pass

    async def _read_events(self, events) -> None:
        decoder = codecs.getincrementaldecoder("utf-8")("replace")
        pending = ""
        async for event in events:
            data = getattr(event, "data", None)
            if not data:
                continue
            pending += decoder.decode(data)
            while "\n" in pending:
                line, pending = pending.split("\n", 1)
                self._publish_message(line.rstrip("\r"))


def describe_error(error: BaseException) -> str:
    """Include nested causes hidden by ExceptionGroup's default string."""
    nested = getattr(error, "exceptions", None)
    if nested:
        return "; ".join(describe_error(item) for item in nested)
    return "{0}: {1}".format(type(error).__name__, error)


def find_pb_command() -> str | None:
    """Find pb in PATH or alongside the Python interpreter running this file."""
    scripts_dir = Path(sys.executable).resolve().parent
    candidates = [scripts_dir / "pb.exe", scripts_dir / "pb"]

    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)

    return shutil.which("pb")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload the EV3 command server and control it over Bluetooth Classic."
    )
    parser.add_argument(
        "--hub",
        default=DEFAULT_HUB_NAME,
        help=f"Pybricks hub name (default: {DEFAULT_HUB_NAME!r})",
    )
    args = parser.parse_args()

    pb = find_pb_command()
    if pb is None:
        print(
            "Could not find the 'pb' command. Install pybricks-cli in this Python "
            "environment, then run this script again.",
            file=sys.stderr,
        )
        return 2

    if not BRICK_PROGRAM.is_file():
        print(f"Brick program not found: {BRICK_PROGRAM}", file=sys.stderr)
        return 2

    print(f"Connecting to {args.hub!r} over Bluetooth Classic (RFCOMM)...")

    # Drop any remembered connection first so the explicit RFCOMM connection
    # below cannot silently reuse a BLE connection from an earlier session.
    subprocess.run(
        [pb, "disconnect", "--hub", args.hub],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    connected = subprocess.run(
        [pb, "connect", "--hub", args.hub, "--transport", "rfcomm"],
        check=False,
    )
    if connected.returncode != 0:
        print("Could not connect to the EV3 over RFCOMM.", file=sys.stderr)
        return connected.returncode

    print("Uploading the brick controller. Type 'help' at the EV3> prompt.")
    try:
        result = subprocess.run(
            [pb, "run", str(BRICK_PROGRAM), "--hub", args.hub],
            check=False,
        )
    except KeyboardInterrupt:
        subprocess.run([pb, "stop", "--hub", args.hub], check=False)
        return 130

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
