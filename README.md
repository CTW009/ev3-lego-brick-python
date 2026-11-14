# EV3 LEGO Brick — Pybricks MicroPython

Beginner-friendly Python examples for the **LEGO MINDSTORMS EV3** running **Pybricks MicroPython v2.0** (the EV3-specific runtime).

> **Hardware note:** Check every motor and sensor port against your robot before running an example. The samples assume motors on B/C and sensors on S1–S4 only where stated. Start with `main.py`, which only uses the display and speaker.

## Quick start

1. Prepare an EV3 microSD card with the official EV3 MicroPython image. **Flashing erases the card**, so back up any programs first.
2. Install Visual Studio Code and the official **LEGO MINDSTORMS EV3 MicroPython** extension.
3. In VS Code, use the extension's **Create a new project** command, or open an existing EV3 MicroPython project folder.
4. Copy this repository's example files into that project folder. The program transferred and run by the extension is normally `main.py`.
5. Turn on the EV3, connect it to the computer with the mini-USB cable, select/configure the USB connection in the extension, then press **F5** to transfer and run.
6. Begin with the safe display/speaker check in `main.py`. Attach motors and sensors only when trying the corresponding example.

See [VS Code setup and running programs](docs/vscode.md) for the full workflow.

## Examples

- `main.py` — safe first-run check: EV3 display and speaker only.
- [Hello brick](examples/hello_brick.py) — display and speaker.
- [Motor basics](examples/motor_basics.py) — one Large Motor on B.
- [Drive straight and turn](examples/drive_base.py) — Large Motors on B/C; calibrate wheel diameter and axle track.
- [Sensors](examples/sensors.py) — touch, color, ultrasonic and infrared examples; match ports to your build.
- `test_ev3.py` — a repeatable hardware smoke test (display, speaker and optional color sensor).

## Documentation

- [VS Code setup and run workflow](docs/vscode.md)
- [API quick reference](docs/api-reference.md)
- [Variables and Python basics](docs/variables-and-python.md)

## Runtime compatibility

This repository targets the **EV3 Pybricks MicroPython 2.0** runtime installed by the EV3 microSD image. It is not the same runtime/API as Pybricks 3.x on newer Powered Up, SPIKE or MINDSTORMS Inventor hubs. EV3 programs run on the brick; a normal desktop CPython interpreter cannot execute the `pybricks.*` hardware modules.

The legacy LEGO EV3 MicroPython VS Code extension is the documented EV3 project-transfer workflow. Follow the setup guide for the EV3-specific image and extension rather than installing `pybricksdev` or a Pybricks 3.x package intended for other hubs.

## PC control over Bluetooth Classic

`Robot/pc_controller.py` uploads and runs `Robot/brick_controller.py` each time it starts. It uses Bluetooth Classic RFCOMM explicitly, not Bluetooth Low Energy. These two scripts target the newer Pybricks 4.1 EV3 firmware and do not run on the EV3 MicroPython v2 SD-card image used by the older examples above.

Install Pybricks CLI into the project virtual environment, pair the EV3 in Windows Bluetooth settings, and turn the brick on. The command-line controller remains available:

```powershell
.\venv\Scripts\python.exe -m pip install pybricks-cli
.\venv\Scripts\python.exe Robot\pc_controller.py --hub "YOUR EV3 NAME"
```

Change `--hub` to match the name displayed by the EV3 if it was given a custom name. The terminal becomes the control console after upload. Type `help` there for motor rotation, timed run, stop, encoder reset, telemetry, and status commands. Ports A-D are supported; the motors must be connected to the ports named in each command. `rotate B 360` turns motor B one revolution; `read all` reports motor angle, speed, load, stalled, and done values for ports A-D. `status` also reports battery and EV3 system information. With an EV3 color sensor on input port 1, enter `watch color` to continuously print the detected color and HSV reading (default interval: 250 ms) while continuing to accept motor commands. Use `watch color 500` to slow the stream to 500 ms, or `unwatch` to stop it.

## Modular motor and sensor setup

`Robot/devices.py` owns device initialization and port-based helpers. Edit `MOTOR_PORTS` and `COLOR_SENSOR_PORTS` there to match the build. Set `MOTOR_GEARS` for any motor with a gear train between its shaft and the mechanism output. For example, `{Port.A: [12, 36]}` describes a 12-tooth motor gear driving a 36-tooth output gear. Pybricks then adjusts speed and angle commands for that ratio. Leave a port out of `MOTOR_GEARS` when there is no gear train to account for. The command server initializes those configured devices before starting its task loop. `start PORT [SPEED]` runs one motor continuously in degrees per second; a negative speed reverses it. `duty PORT PERCENT` sets motor output power from -100% to 100%, such as `duty A 20`. The Python interface can also be used by another brick program:

```python
from pybricks.parameters import Port
from devices import initialize_devices, set_motor_duty, start_motor, stop_motor

initialize_devices()  # Call before run_task().
start_motor(Port.A, 360)
set_motor_duty(Port.A, 20)
stop_motor(Port.A)
```

Color sensors are configured by name, such as `{"color": Port.S1}`. Import `get_color_sensor("color")` to access that sensor in another brick module.

To use the Pygame app as a connected PC client, run:

```powershell
.\venv\Scripts\python.exe Robot\main.py
```

The app uploads the brick controller over RFCOMM. It displays the connection status and received text output. The Pygame client sends a heartbeat every 500 ms; if the PC app exits unexpectedly, the EV3 stops all motors and exits the controller after 2.5 seconds without a heartbeat. From Python, `robot_player.rotate_motor("B", 360, 250)` sends a motor move and `robot_player.read_motor_data("all")` requests readings from ports A-D. Call `robot_player.update()` to process new output, then read `robot_player.get_motor_data()`. The result is a dictionary keyed by port, with `angle`, `speed`, `load`, `stalled`, and `done` values. For example, `robot_player.get_motor_data()["A"]["speed"]` returns the latest speed reading for port A.

Use either the Pygame app or the standalone `pc_controller.py` terminal session at a time; both upload and start the same EV3 controller program.

## Official references

- [Pybricks EV3 installation](https://pybricks.com/install/mindstorms-ev3/installation/)
- [Running EV3 MicroPython programs](https://pybricks.com/install/mindstorms-ev3/running-programs/)
- [Pybricks EV3 v2.0 API documentation](https://docs.pybricks.com/en/v2.0/)
- [EV3 devices](https://docs.pybricks.com/en/v2.0/ev3devices.html)
- [EV3 hub](https://docs.pybricks.com/en/v2.0/hubs.html)
- [DriveBase](https://docs.pybricks.com/en/v2.0/robotics.html)

## License

No license is included yet. Choose one before inviting others to reuse or redistribute the project.
