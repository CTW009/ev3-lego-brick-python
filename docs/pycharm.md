# PyCharm and EV3 MicroPython

PyCharm is a Python IDE, but LEGO's EV3 MicroPython v2 workflow in the supplied guide uses Visual Studio Code plus the LEGO EV3 MicroPython extension. The guide's extension creates compatible project folders, connects to the brick over USB, transfers files and runs programs. Do not expect a similarly named PyCharm plugin to provide those LEGO-specific features.

## Recommended arrangement

1. Use PyCharm to edit `.py` files if that is your preferred editor.
2. Use VS Code with the official LEGO EV3 MicroPython extension to create an EV3 project and transfer/run it on the brick.
3. Keep `main.py` at the root of the project folder that the extension downloads to the EV3.

## PyCharm support

PyCharm's Python support is included in the IDE. No extra plugin is needed to edit Python. The optional **IdeaVim** and generic Python plugins are not EV3 deployment support. The EV3 MicroPython extension is a VS Code extension and cannot be installed into PyCharm.

## Interpreter and code completion

The Pybricks EV3 runtime runs on the brick, not the computer's standard CPython interpreter. A local Python interpreter can check basic syntax, but it cannot import the EV3 runtime modules unless separate stubs/packages are configured. Do not `pip install` regular Pybricks packages and assume that enables EV3 transfer or accurately emulates brick hardware.

For a comfortable PyCharm editing setup, open this folder and set a Python 3 interpreter for basic editing. For actual EV3 hardware tests, transfer and run through the LEGO VS Code extension, or follow the Pybricks documentation for the exact EV3 image.

## References

- [LEGO setup guide](https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltb470b9ea6e38f8d4/5f8802fc4376310c19e33714/getting-started-with-micropython-v2_enus.pdf?locale=en-us)
- [LEGO EV3 MicroPython VS Code extension](https://marketplace.visualstudio.com/items?itemName=lego-education.ev3-micropython)
- [Pybricks EV3 documentation](https://docs.pybricks.com/en/v2.0/)
