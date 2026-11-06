#!/usr/bin/env pybricks-micropython
"""Sensor examples. Uncomment only the sensor connected to the chosen port."""

from pybricks.ev3devices import (
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait

ev3 = EV3Brick()

# Change each port to match your actual cable. Use one appropriate sensor per
# input port; not all sensors need to be attached at once.
touch = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
ultrasonic = UltrasonicSensor(Port.S3)
infrared = InfraredSensor(Port.S4)
# gyro = GyroSensor(Port.S1)  # Substitute for touch if gyro is on S1.

while True:
    pressed = touch.pressed()
    detected_color = color_sensor.color()
    distance_mm = ultrasonic.distance()
    beacon_reading = infrared.beacon(1)

    ev3.screen.clear()
    ev3.screen.print("Touch:", pressed)
    ev3.screen.print("Color:", detected_color)
    ev3.screen.print("Distance mm:", distance_mm)
    ev3.screen.print("Beacon:", beacon_reading)

    if pressed:
        ev3.speaker.beep(1000, 100)
        break
    wait(100)
