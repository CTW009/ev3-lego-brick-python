#!/usr/bin/env pybricks-micropython
"""Wait for a color sensor flag, then drive while monitoring the sensor.

Requires Pybricks firmware 3.3 or newer (the multitasking API is not in v2.0).
Assumes motors on A/D and a color sensor on S1; change ports to match your robot.
"""

from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Color, Port
from pybricks.tools import multitask, run_task, wait

left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
color_sensor = ColorSensor(Port.S1)
start_flag = False


async def drive_when_flag_is_set():
    """Wait for the sensor task to set the flag, then drive for three seconds."""
    global start_flag
    print("Waiting for the color sensor to see red...")
    while not start_flag:
        await wait(10)  # Yield so the sensor task can check the color.

    print("Flag set; driving.")
    left_motor.run(300)
    right_motor.run(-300)
    await wait(3000)


async def watch_for_red():
    """Set the shared flag when red is detected."""
    global start_flag
    while not start_flag:
        detected_color = await color_sensor.color()
        print("Color:", detected_color)
        if detected_color == Color.RED:
            start_flag = True
        else:
            await wait(100)


async def main():
    global start_flag
    while True:
        start_flag = False
        try:
            # The drive task waits for the sensor task to set start_flag.
            await multitask(drive_when_flag_is_set(), watch_for_red())
        finally:
            left_motor.brake()
            right_motor.brake()


run_task(main())
