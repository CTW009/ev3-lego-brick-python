#!/usr/bin/env pybricks-micropython
"""Safe first-run check for an EV3 running Pybricks MicroPython 2.0.

This program uses only the display and speaker. It does not move motors.
"""

from pybricks.hubs import EV3Brick
from pybricks.tools import wait

ev3 = EV3Brick()

ev3.screen.clear()
ev3.screen.print("EV3 Pybricks OK")
ev3.speaker.beep(frequency=800, duration=200)
wait(500)
ev3.screen.print("Ready for code!")
