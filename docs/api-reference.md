# EV3 MicroPython API quick reference

This reference covers the APIs used by the starter examples, from the official Pybricks MicroPython 2.0 documentation. It is a practical index, not an exhaustive listing of every method in every module. Use linked official docs for version-specific details.

## Main modules and classes

- `pybricks.hubs.EV3Brick`: brick screen, speaker, buttons and lights.
- `pybricks.ev3devices.Motor`: motor with rotation sensor.
- `pybricks.ev3devices.TouchSensor`, `ColorSensor`, `UltrasonicSensor`, `InfraredSensor`, `GyroSensor`: EV3 input devices.
- `pybricks.robotics.DriveBase`: coordinated two-wheel robot movement.
- `pybricks.parameters.Port`: motor/sensor port constants.
- `pybricks.parameters.Stop`, `Direction`, `Color`, `Button`: option/value enums.
- `pybricks.tools.wait`: pause in milliseconds.

## Methods used in examples

| API | Inputs | Result / effect |
|---|---|---|
| `EV3Brick()` | none | Create the EV3 brick interface. |
| `ev3.screen.clear()` | none | Clear the display. |
| `ev3.screen.print(*values)` | printable values | Show text on display. |
| `ev3.speaker.beep(frequency=500, duration=100)` | Hz, ms | Play a tone. |
| `ev3.light.on(color)` | `Color` | Set status light. |
| `Motor(port, positive_direction=..., gears=...)` | port and optional direction/gearing | Create motor object. |
| `motor.run(speed)` | deg/s | Run continuously until another command. |
| `motor.run_time(speed, time, then=Stop.HOLD, wait=True)` | deg/s, ms, stop behavior, wait flag | Run for a duration. |
| `motor.run_angle(speed, rotation_angle, then=Stop.HOLD, wait=True)` | deg/s, relative degrees | Rotate by an amount. |
| `motor.run_target(speed, target_angle, then=Stop.HOLD, wait=True)` | deg/s, absolute degrees | Move to target angle. |
| `motor.run_until_stalled(speed, then=Stop.COAST, duty_limit=None)` | deg/s, stop behavior, optional duty % | Run until stalled; returns stall angle. Use only with a safe mechanism. |
| `motor.stop()` | none | Stop and coast. |
| `motor.brake()` | none | Passively brake. |
| `motor.hold()` | none | Actively hold current position. |
| `motor.speed()` / `motor.angle()` | none | Read deg/s / degrees. |
| `motor.reset_angle(angle)` | degrees | Set reported motor angle. |
| `DriveBase(left_motor, right_motor, wheel_diameter, axle_track)` | motors, mm, mm | Create drive base; axle track is center-to-center wheel distance. |
| `drive_base.straight(distance)` | mm | Drive forward (positive) or backward (negative). |
| `drive_base.turn(angle)` | degrees | Turn in place. |
| `drive_base.drive(speed, turn_rate)` | mm/s, deg/s | Continuous steering. |
| `drive_base.stop()` | none | Stop the drive base and let the motors spin freely. |
| `drive_base.settings(...)` | optional speed/acceleration settings | Get or change motion settings. |
| `TouchSensor(port).pressed()` | port | `True` while pressed. |
| `ColorSensor(port).color()` | port | `Color` enum or `None`. |
| `ColorSensor(port).reflection()` | port | Reflected red light percentage, 0-100. |
| `ColorSensor(port).ambient()` | port | Ambient light percentage, 0-100. |
| `ColorSensor(port).rgb()` | port | `(red, green, blue)` percentages. |
| `UltrasonicSensor(port).distance(silent=False)` | port, optional flag | Distance in mm. |
| `UltrasonicSensor(port).presence()` | port | Whether ultrasonic sound is detected. |
| `InfraredSensor(port).distance()` | port | Relative distance percentage. |
| `InfraredSensor(port).beacon(channel)` | channel 1-4 | `(relative_distance, angle)` or `(None, None)`. |
| `InfraredSensor(port).buttons(channel)` / `.keypad()` | channel for `buttons` | List of pressed remote buttons; `keypad()` uses channel 1 behavior. |
| `GyroSensor(port).angle()` / `.speed()` | port | Accumulated degrees / angular velocity deg/s. Avoid reading both: `speed()` resets angle. |
| `wait(time)` | milliseconds | Pause the program. |

## EV3 API method index

This index lists the public methods for the EV3-specific classes referenced here in Pybricks MicroPython 2.0. It does not include generic Python built-ins or every method from unrelated Pybricks modules.

### `EV3Brick`

- `buttons.pressed()` returns the list of currently pressed brick buttons.
- `light.on(color)` sets the status light; `light.off()` turns it off.
- `speaker.beep(frequency=500, duration=100)` plays a tone.
- `speaker.play_notes(notes, tempo=120)` plays a sequence of musical notes.
- `speaker.play_file(file_name)` plays an audio file on the brick.
- `speaker.say(text)` speaks text using configured speech settings.
- `speaker.set_speech_options(language=None, voice=None, speed=None, pitch=None)` sets speech settings for `say`.
- `screen.clear()` clears the display; `screen.print(*values)` displays text.

### `Motor`

- Read/reset: `speed()`, `angle()`, `reset_angle(angle)`.
- Stop: `stop()`, `brake()`, `hold()`.
- Motion: `run(speed)`, `run_time(speed, time, then=Stop.HOLD, wait=True)`, `run_angle(speed, rotation_angle, then=Stop.HOLD, wait=True)`, `run_target(speed, target_angle, then=Stop.HOLD, wait=True)`, `run_until_stalled(speed, then=Stop.COAST, duty_limit=None)`, `dc(duty)`.
- Advanced target control: `track_target(target_angle)` and the `control` attribute (PID settings are documented on the Control class page).

### EV3 input devices

- `TouchSensor`: `pressed()`.
- `ColorSensor`: `color()`, `ambient()`, `reflection()`, `rgb()`.
- `UltrasonicSensor`: `distance(silent=False)`, `presence()`.
- `InfraredSensor`: `distance()`, `beacon(channel)`, `buttons(channel)`, `keypad()`.
- `GyroSensor`: `speed()`, `angle()`, `reset_angle(angle)`. Do not call `speed()` in a program that relies on `angle()`; reading angular speed resets the accumulated angle.

### `DriveBase`

- Drive: `straight(distance)`, `turn(angle)`, `drive(drive_speed, turn_rate)`, `stop()`.
- Configure and measure: `settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)`, `distance()`, `angle()`, `state()`, `reset()`.
- `state()` returns `(distance_mm, drive_speed_mm_per_s, angle_degrees, turn_rate_deg_per_s)`.

### `StopWatch` and `DataLog` (optional tools)

- `StopWatch`: `time()`, `pause()`, `resume()`, `reset()`.
- `DataLog(*headers, name='log', timestamp=True, extension='csv', append=False)`: create a log file; call `log(*values)` to append a row.

### Variables declared by the examples

The examples declare no custom functions (`def`). Their variables are listed in [variables-and-python.md](variables-and-python.md), including imports/objects and configurable constants. Python built-ins such as `True`, `None`, `print` and `range` are language features, not EV3 API variables.

## Basic pattern

```python
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

ev3 = EV3Brick()
motor = Motor(Port.B)
ev3.speaker.beep()
motor.run_target(500, 90)  # 500 deg/s to absolute angle 90 degrees
ev3.screen.print("Done")
```

`run_target` uses an absolute target angle; `run_angle` uses relative rotation. Use `wait=False` only when you intend to issue another command while the motor moves.

## Further official APIs

- [EV3 devices (motor and sensor methods)](https://docs.pybricks.com/en/v2.0/ev3devices.html)
- [Hubs, screen, speaker, buttons, light](https://docs.pybricks.com/en/v2.0/hubs.html)
- [DriveBase and robotics](https://docs.pybricks.com/en/v2.0/robotics.html)
- [Parameters and enums](https://docs.pybricks.com/en/v2.0/parameters.html)
- [Tools, including wait](https://docs.pybricks.com/en/v2.0/tools.html)
- [LEGO guide: connecting, transfer and run](https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltb470b9ea6e38f8d4/5f8802fc4376310c19e33714/getting-started-with-micropython-v2_enus.pdf?locale=en-us)
