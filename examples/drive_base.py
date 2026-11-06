#!/usr/bin/env pybricks-micropython
"""Drive forward and turn using Large Motors on B and C."""

from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Measure these on your robot. Values shown fit many common EV3 builds but
# must be calibrated for your wheels and chassis.
WHEEL_DIAMETER = 56  # mm
AXLE_TRACK = 120     # mm, center-to-center between the wheels

drive_base = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
drive_base.straight(300)  # 300 mm forward
drive_base.turn(90)       # 90 degrees in place
drive_base.stop()
