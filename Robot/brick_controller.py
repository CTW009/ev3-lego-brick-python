"""Command and telemetry server for a Pybricks 4.1 EV3 Brick.

Commands are entered in the connected PC terminal. Use ``help`` for the
command list. Motor output ports A-D are supported; change the port mapping
below if your build uses a different arrangement.
"""

from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import StopWatch, read_input_byte, run_task, wait
from devices import (
    get_color_sensor as device_color_sensor,
    get_motor as device_motor,
    initialize_devices,
    set_motor_duty,
    start_motor,
    stop_all_motors,
    stop_motor as device_stop_motor,
)


DEFAULT_SPEED = 360  # degrees per second
MAX_SPEED = 1000  # degrees per second
MAX_TIMED_RUN_MS = 60000

PORTS = {
    "A": Port.A,
    "B": Port.B,
    "C": Port.C,
    "D": Port.D,
}

ev3 = EV3Brick()
color_watch_interval_ms = None
color_watch_timer = StopWatch()
connection_watchdog_interval_ms = None
connection_watchdog_timer = StopWatch()


def get_motor(port_name):
    port_name = port_name.upper()
    if port_name not in PORTS:
        raise ValueError("motor port must be A, B, C, or D")
    return device_motor(PORTS[port_name])


def get_color_sensor():
    return device_color_sensor()


def stop_motor(port_name):
    device_stop_motor(PORTS[port_name.upper()])


def print_motor_info(port_name):
    try:
        motor = get_motor(port_name)
        print(
            "MOTOR|{0}|{1}|{2}|{3}|{4}|{5}".format(
                port_name, motor.angle(), motor.speed(), motor.load(),
                int(motor.stalled()), int(motor.done())
            )
        )
    except Exception as error:
        print("{0}: unavailable ({1})".format(port_name, error))


def print_all_motor_info():
    for port_name in ("A", "B", "C", "D"):
        print_motor_info(port_name)


def print_status():
    print(
        "Battery: voltage={0} mV, current={1} mA".format(
            ev3.battery.voltage(), ev3.battery.current()
        )
    )
    print("EV3 system: {0}".format(ev3.system.info()))
    print_all_motor_info()


async def print_color_reading():
    sensor = get_color_sensor()
    detected = await sensor.color()
    hsv = await sensor.hsv()
    print("Color S1: detected={0}, HSV={1}".format(detected, hsv))


async def watch_color(interval_ms):
    global color_watch_interval_ms
    color_watch_interval_ms = interval_ms
    color_watch_timer.reset()
    print("Color stream on S1 every {0} ms. Type 'unwatch' to stop it.".format(interval_ms))
    try:
        await print_color_reading()
    except Exception:
        color_watch_interval_ms = None
        raise


def require_motor_port(words):
    if len(words) < 2:
        raise ValueError("specify a motor port: A, B, C, or D")
    return words[1].upper()


async def handle_command(line):
    global connection_watchdog_interval_ms
    words = line.strip().split()
    if not words:
        return True

    connection_watchdog_timer.reset()
    command = words[0].lower()

    if command == "heartbeat":
        return True

    if command == "watchdog":
        if len(words) != 2:
            raise ValueError("usage: watchdog TIMEOUT_MS")
        timeout_ms = int(words[1])
        if timeout_ms < 1000 or timeout_ms > 10000:
            raise ValueError("watchdog timeout must be between 1000 and 10000 ms")
        connection_watchdog_interval_ms = timeout_ms
        connection_watchdog_timer.reset()
        print("PC connection watchdog enabled ({0} ms).".format(timeout_ms))
        return True

    if command in ("help", "?"):
        print("Commands:")
        print("  start PORT [SPEED]           run motor continuously; negative speed reverses")
        print("  duty PORT PERCENT            set motor power from -100 to 100 percent")
        print("  rotate PORT DEGREES [SPEED]  relative rotation; degrees may be negative")
        print("  target PORT ANGLE [SPEED]    rotate to an absolute encoder angle")
        print("  timed PORT SPEED MS          run at deg/s for a bounded duration")
        print("  stop PORT|all                stop one motor or all initialized motors")
        print("  reset PORT [ANGLE]           set the encoder reading")
        print("  read PORT|all                read angle, speed, load, stalled, and done")
        print("  color                        read the color sensor on input port 1 once")
        print("  watch color [INTERVAL_MS]    stream detected color and HSV continuously")
        print("  unwatch                      stop the color stream")
        print("  status                       battery, EV3 system info, and motors A-D")
        print("  quit                         stop motors and end this program")
        print("  Motor ports: A, B, C, D. Defaults: speed={0} deg/s.".format(DEFAULT_SPEED))
        return True

    if command in ("quit", "exit"):
        stop_all_motors()
        print("Motors stopped. Disconnecting.")
        return False

    if command == "status":
        print_status()
        return True

    if command == "color":
        await print_color_reading()
        return True

    if command == "watch":
        if len(words) < 2 or words[1].lower() != "color" or len(words) > 3:
            raise ValueError("usage: watch color [INTERVAL_MS]")
        interval_ms = int(words[2]) if len(words) == 3 else 250
        if interval_ms < 50 or interval_ms > 5000:
            raise ValueError("interval must be between 50 and 5000 ms")
        await watch_color(interval_ms)
        return True

    if command == "unwatch":
        global color_watch_interval_ms
        color_watch_interval_ms = None
        print("Color stream stopped.")
        return True

    if command == "read":
        if len(words) < 2:
            raise ValueError("usage: read PORT|all")
        if words[1].lower() == "all":
            print_all_motor_info()
        else:
            print_motor_info(require_motor_port(words))
        return True

    if command == "stop":
        if len(words) < 2:
            raise ValueError("usage: stop PORT|all")
        if words[1].lower() == "all":
            stop_all_motors()
            print("All initialized motors stopped.")
        else:
            port_name = require_motor_port(words)
            stop_motor(port_name)
            print("Motor {0} stopped.".format(port_name))
        return True

    if command == "start":
        if len(words) not in (2, 3):
            raise ValueError("usage: start PORT [SPEED]")
        port_name = require_motor_port(words)
        speed = int(words[2]) if len(words) == 3 else DEFAULT_SPEED
        if speed == 0 or abs(speed) > MAX_SPEED:
            raise ValueError("speed must be between -{0} and {0} deg/s, excluding 0".format(MAX_SPEED))
        start_motor(PORTS[port_name], speed)
        print("Started motor {0} at {1} deg/s.".format(port_name, speed))
        return True

    if command == "duty":
        if len(words) != 3:
            raise ValueError("usage: duty PORT PERCENT")
        port_name = require_motor_port(words)
        duty = int(words[2])
        set_motor_duty(PORTS[port_name], duty)
        print("Set motor {0} duty cycle to {1}%.".format(port_name, duty))
        return True

    if command == "reset":
        port_name = require_motor_port(words)
        angle = int(words[2]) if len(words) > 2 else 0
        motor = get_motor(port_name)
        motor.reset_angle(angle)
        print_motor_info(port_name)
        return True

    if command in ("rotate", "target"):
        if len(words) not in (3, 4):
            raise ValueError("usage: {0} PORT DEGREES [SPEED]".format(command))

        port_name = require_motor_port(words)
        degrees = int(words[2])
        speed = int(words[3]) if len(words) == 4 else DEFAULT_SPEED
        if speed <= 0 or speed > MAX_SPEED:
            raise ValueError("speed must be between 1 and {0} deg/s".format(MAX_SPEED))

        motor = get_motor(port_name)
        if command == "rotate":
            await motor.run_angle(speed, degrees, wait=False)
        else:
            await motor.run_target(speed, degrees, wait=False)

        print("Started {0} on motor {1}.".format(command, port_name))
        print_motor_info(port_name)
        return True

    if command == "timed":
        if len(words) != 4:
            raise ValueError("usage: timed PORT SPEED MS")

        port_name = require_motor_port(words)
        speed = int(words[2])
        duration_ms = int(words[3])
        if speed == 0 or abs(speed) > MAX_SPEED:
            raise ValueError("speed must be between -{0} and {0} deg/s, excluding 0".format(MAX_SPEED))
        if duration_ms <= 0 or duration_ms > MAX_TIMED_RUN_MS:
            raise ValueError("duration must be between 1 and {0} ms".format(MAX_TIMED_RUN_MS))

        motor = get_motor(port_name)
        await motor.run_time(speed, duration_ms, wait=False)
        print("Started motor {0} at {1} deg/s for {2} ms.".format(port_name, speed, duration_ms))
        print_motor_info(port_name)
        return True

    raise ValueError("unknown command; type 'help' for the command list")


async def main():
    global color_watch_interval_ms, connection_watchdog_interval_ms
    print("EV3 controller ready. Type 'help' for commands.")
    print("EV3> ", end="")
    line_buffer = ""
    previous_was_carriage_return = False
    keep_running = True

    while keep_running:
        received = read_input_byte()
        if received is not None:
            char = chr(received) if isinstance(received, int) else received

            if char in ("\r", "\n"):
                if char == "\n" and previous_was_carriage_return:
                    previous_was_carriage_return = False
                else:
                    previous_was_carriage_return = char == "\r"
                    print()
                    try:
                        keep_running = await handle_command(line_buffer)
                    except (ValueError, TypeError) as error:
                        print("Error: {0}".format(error))
                    except Exception as error:
                        print("Command failed: {0}".format(error))
                    line_buffer = ""
                    if keep_running:
                        print("EV3> ", end="")
            else:
                previous_was_carriage_return = False
                if char in ("\b", "\x7f"):
                    line_buffer = line_buffer[:-1]
                elif char >= " " and char != "\x7f":
                    line_buffer += char

        if color_watch_interval_ms is not None and color_watch_timer.time() >= color_watch_interval_ms:
            try:
                await print_color_reading()
            except Exception as error:
                color_watch_interval_ms = None
                print("Color stream stopped: {0}".format(error))
            color_watch_timer.reset()

        if (
            connection_watchdog_interval_ms is not None
            and connection_watchdog_timer.time() >= connection_watchdog_interval_ms
        ):
            print("PC connection lost. Stopping all motors.")
            color_watch_interval_ms = None
            connection_watchdog_interval_ms = None
            keep_running = False

        await wait(10)

    stop_all_motors()


# Pybricks requires devices to be initialized before run_task() starts.
initialize_devices()

run_task(main())
