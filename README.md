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

## Official references

- [LEGO: Getting started with EV3 MicroPython v2 (PDF)](https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltb470b9ea6e38f8d4/5f8802fc4376310c19e33714/getting-started-with-micropython-v2_enus.pdf?locale=en-us)
- [Pybricks v2.0 documentation](https://docs.pybricks.com/en/v2.0/)
- [EV3 devices API](https://docs.pybricks.com/en/v2.0/ev3devices.html)
- [EV3 parameters](https://docs.pybricks.com/en/v2.0/parameters.html)
- [EV3 hub](https://docs.pybricks.com/en/v2.0/hubs.html)
- [DriveBase](https://docs.pybricks.com/en/v2.0/robotics.html)

## License

No license is included yet. Choose one before inviting others to reuse or redistribute the project.
