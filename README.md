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

## Official references

- [Pybricks EV3 installation](https://pybricks.com/install/mindstorms-ev3/installation/)
- [Running EV3 MicroPython programs](https://pybricks.com/install/mindstorms-ev3/running-programs/)
- [Pybricks EV3 v2.0 API documentation](https://docs.pybricks.com/en/v2.0/)
- [EV3 devices](https://docs.pybricks.com/en/v2.0/ev3devices.html)
- [EV3 hub](https://docs.pybricks.com/en/v2.0/hubs.html)
- [DriveBase](https://docs.pybricks.com/en/v2.0/robotics.html)

## License

No license is included yet. Choose one before inviting others to reuse or redistribute the project.
