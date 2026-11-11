from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port


# Edit these lists to initialize only the devices installed on your robot.
MOTOR_PORTS = (Port.A, Port.D)
# Optional gear trains, listed from the motor shaft toward the output shaft.
# Example: Port.A: [12, 36] means a 12-tooth gear drives a 36-tooth gear.
MOTOR_GEARS = {Port.A: [12,20],Port.D: [12,20]}
COLOR_SENSOR_PORTS = {"color": Port.S1}

motors = {}
motor_errors = {}
color_sensors = {}
color_sensor_errors = {}


def initialize_devices():
    """Initialize the devices configured above. Call before run_task()."""
    for port in MOTOR_PORTS:
        try:
            gears = MOTOR_GEARS.get(port)
            if gears:
                motors[port] = Motor(port, gears=gears)
            else:
                motors[port] = Motor(port)
        except Exception as error:
            motor_errors[port] = error

    for name, port in COLOR_SENSOR_PORTS.items():
        try:
            color_sensors[name] = ColorSensor(port)
        except Exception as error:
            color_sensor_errors[name] = error


def get_motor(port):
    if port not in MOTOR_PORTS:
        raise ValueError("motor port is not configured: {0}".format(port))
    if port not in motors:
        raise RuntimeError("Motor on {0} is unavailable: {1}".format(port, motor_errors.get(port, "not initialized")))
    return motors[port]


def start_motor(port, speed=360):
    """Run one configured motor continuously at ``speed`` degrees/second."""
    get_motor(port).run(speed)


def set_motor_duty(port, duty):
    """Set one configured motor's duty cycle from -100% to 100%."""
    if duty < -100 or duty > 100:
        raise ValueError("duty cycle must be between -100 and 100 percent")
    get_motor(port).dc(duty)


def stop_motor(port):
    get_motor(port).stop()


def stop_all_motors():
    for motor in motors.values():
        motor.brake()


def get_color_sensor(name="color"):
    if name not in COLOR_SENSOR_PORTS:
        raise ValueError("color sensor is not configured: {0}".format(name))
    if name not in color_sensors:
        raise RuntimeError("Color sensor '{0}' is unavailable: {1}".format(name, color_sensor_errors.get(name, "not initialized")))
    return color_sensors[name]
