#!/usr/bin/env pybricks-micropython
"""EV3 hardware smoke test for Pybricks MicroPython 2.0.

The display and speaker checks always run. The color sensor check is optional:
connect a supported EV3 Color Sensor to S1 before enabling USE_COLOR_SENSOR.
No motors are moved by this test.
"""

from pybricks.hubs import EV3Brick
from pybricks.tools import wait

# Set True only when a Color Sensor is physically connected to input port S1.
USE_COLOR_SENSOR = False

ev3 = EV3Brick()
ev3.screen.clear()
ev3.screen.print("EV3 hardware test")

# Speaker check.
ev3.speaker.beep(frequency=880, duration=200)
wait(300)

if USE_COLOR_SENSOR:
    from pybricks.ev3devices import ColorSensor
    from pybricks.parameters import Port

    color_sensor = ColorSensor(Port.S1)
    detected_color = color_sensor.color()
    ev3.screen.print("Color:", detected_color)
else:
    ev3.screen.print("Color sensor: skipped")

ev3.screen.print("Test complete")
ev3.speaker.beep(frequency=1200, duration=150)
