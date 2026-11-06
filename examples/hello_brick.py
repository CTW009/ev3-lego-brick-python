#!/usr/bin/env pybricks-micropython
"""Say hello using the EV3 display and speaker."""

from pybricks.hubs import EV3Brick
from pybricks.tools import wait

ev3 = EV3Brick()
ev3.screen.clear()
ev3.screen.print("Hello, EV3!")
ev3.speaker.beep(800, 300)
wait(1000)
