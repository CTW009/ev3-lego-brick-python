#!/usr/bin/env pybricks-micropython
"""Rotate a Large Motor on output B by 360 degrees."""

from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port

ev3 = EV3Brick()
motor = Motor(Port.B)  # Change Port.B to match the physical connection.

ev3.speaker.beep()
motor.run_angle(400, 360)  # 400 deg/s, relative rotation of 360 degrees.
ev3.speaker.beep(1000, 200)
