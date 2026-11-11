# EV3 Lego Brick (MicroPython)

A beginner-friendly Python project for the LEGO MINDSTORMS Education EV3 Brick using LEGO EV3 MicroPython v2 / Pybricks 2.0.0.

> The folder was empty when this documentation was added. These are starter programs, not a description of existing robot wiring. Check port constants before running motor or sensor examples.

## Quick start

1. Use the prepared EV3 MicroPython microSD card in the brick.
2. Install the [LEGO EV3 MicroPython VS Code extension](https://marketplace.visualstudio.com/items?itemName=lego-education.ev3-micropython) for the project transfer workflow described in the [LEGO setup guide](https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltb470b9ea6e38f8d4/5f8802fc4376310c19e33714/getting-started-with-micropython-v2_enus.pdf?locale=en-us).
3. Open this folder as an EV3 MicroPython project, or copy an example into a project created with the extension.
4. Confirm physical ports before running. Samples assume motors on B/C and sensors on S1-S4 only where stated.
5. Connect the running brick by USB and use the extension's device browser/run commands.

The LEGO guide describes VS Code and the EV3 MicroPython extension. PyCharm edits Python files but does not provide LEGO's EV3 project deployment workflow. See [docs/pycharm.md](docs/pycharm.md).

## Examples

- [Hello brick](examples/hello_brick.py): display and speaker.
- [Motor basics](examples/motor_basics.py): one Large Motor on B.
- [Drive straight and turn](examples/drive_base.py): Large Motors on B/C.
- [Sensor examples](examples/sensors.py): touch, color, ultrasonic, infrared and gyro examples; match ports to your build.

## Documentation

- [API methods and parameters](docs/api-reference.md)
- [Variables and Python basics](docs/variables-and-python.md)
- [PyCharm setup and limitation](docs/pycharm.md)

## Runtime notes

These examples use `pybricks-micropython` 2.0.0, the runtime described by the LEGO guide. They target the EV3 MicroPython SD-card image, not newer Powered Up hubs or the Pybricks Code browser workflow.

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

- [LEGO: Getting started with EV3 MicroPython v2 (PDF)](https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltb470b9ea6e38f8d4/5f8802fc4376310c19e33714/getting-started-with-micropython-v2_enus.pdf?locale=en-us)
- [Pybricks v2.0 documentation](https://docs.pybricks.com/en/v2.0/)
- [EV3 devices API](https://docs.pybricks.com/en/v2.0/ev3devices.html)
- [EV3 parameters](https://docs.pybricks.com/en/v2.0/parameters.html)
- [EV3 hub](https://docs.pybricks.com/en/v2.0/hubs.html)
- [DriveBase](https://docs.pybricks.com/en/v2.0/robotics.html)

## License

No license is included yet. Choose one before inviting others to reuse or redistribute the project.
