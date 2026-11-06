# Variables and Python basics

The project folder contained no Python source files at setup time, so there were no pre-existing user variables to inventory. This page explains the variables used in the starter examples and the naming pattern for new programs.

## Variables in the examples

| Name | Example type | Meaning |
|---|---|---|
| `ev3` | `EV3Brick` | Handle for the brick display, speaker and status light. |
| `motor`, `left_motor`, `right_motor` | `Motor` | Motor handles; use the correct output port. |
| `drive_base` | `DriveBase` | Coordinates the left and right motors. |
| `WHEEL_DIAMETER` | number (mm) | Wheel diameter; measure the actual wheel. |
| `AXLE_TRACK` | number (mm) | Center-to-center distance between drive wheels. |
| `SPEED` | number (deg/s or mm/s, method-dependent) | Suggested name for a motion rate constant; not currently declared in the examples. |
| `TOUCH_PORT`, `COLOR_PORT`, etc. | `Port` enum | Suggested names for sensor port constants; the examples currently pass `Port.S1` etc. directly. |
| `touch`, `color_sensor`, `ultrasonic`, `infrared`, `gyro` | sensor classes | Handles for connected input devices. |
| `distance_mm` | number or `None` | Ultrasonic distance measurement. |
| `pressed` | `bool` | Touch sensor state. |
| `detected_color` | `Color` enum or `None` | Color sensor reading. |
| `channel` | `int` | Infrared remote channel (typically 1-4). |
| `rgb_values` | 3-item tuple | Red, green, blue reflection percentages. |
| `beacon_reading` | tuple | IR beacon distance and angle, or `(None, None)` when unavailable. |

The actual starter scripts declare `ev3`, `motor`, `left_motor`, `right_motor`, `WHEEL_DIAMETER`, `AXLE_TRACK`, `drive_base`, `touch`, `color_sensor`, `ultrasonic`, `infrared`, `pressed`, `detected_color`, `distance_mm`, and `beacon_reading`. `gyro` appears as a commented alternative so it does not run alongside the touch sensor on S1. `wait` is an imported function, not a variable created by the program.

Constants use uppercase by convention. Device handles and measurements use lowercase `snake_case`. These are conventions, not special syntax.

## Assignment and values

```python
speed = 400                # integer value
wheel_diameter = 56.0      # decimal value (mm)
robot_ready = True          # boolean
message = "Starting"       # text
```

`=` assigns a value. `==` compares values. Names are case-sensitive: `motor` and `Motor` differ.

## Imports and objects

```python
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

left_motor = Motor(Port.B)
left_motor.run(300)
```

`Motor` is a class imported from a Pybricks module. `left_motor` is an object created from it. `run` is a method called on that object.

## Conditions and loops

```python
if touch.pressed():
    ev3.speaker.beep(1000, 100)

while not touch.pressed():
    left_motor.run(200)
left_motor.brake()
```

A condition chooses whether a block runs. A `while` loop repeats while its condition is true. Indentation defines each block. Include a safe stop condition for continuously running motors.

## Units

- Motor speed: degrees per second (`deg/s`).
- Motor angle: degrees.
- Wait and timed motor duration: milliseconds (`ms`).
- Ultrasonic distance: millimeters (`mm`).
- DriveBase distance and speed: millimeters and millimeters per second.
- Turn angle and rate: degrees and degrees per second.
- Reflected/ambient light: percent.

See [API methods and parameters](api-reference.md) and the [Pybricks API reference](https://docs.pybricks.com/en/v2.0/).
