
from pybricks.ev3devices import Motor
from pybricks.tools import wait
import math
from settings import Hardware, Motors as MotorSettings, Strain


class Motors:

    def __init__(self):
        self.motor1 = Motor(port=Hardware.LEFT_MOTOR_PORT, gears=MotorSettings.LEFT_GEAR)
        self.motor2 = Motor(port=Hardware.RIGHT_MOTOR_PORT, gears=MotorSettings.RIGHT_GEAR)
        self.motor3 = Motor(port=Hardware.RADAR_MOTOR_PORT, gears=MotorSettings.Raydar_GEAR)

        self.motor1.control.limits(
            MotorSettings.CONTROL_SPEED,
            MotorSettings.CONTROL_ACCELERATION,
            MotorSettings.CONTROL_TORQUE_LIMIT
        )
        self.motor2.control.limits(
            MotorSettings.CONTROL_SPEED,
            MotorSettings.CONTROL_ACCELERATION,
            MotorSettings.CONTROL_TORQUE_LIMIT
        )

        self.set_left_speed = 0
        self.set_right_speed = 0

    def speed_L(self, speed):
        self.set_left_speed = abs(speed)
        self.motor1.run(-speed)

    def speed_R(self, speed):
        self.set_right_speed = abs(speed)
        self.motor2.run(speed)

    # def speed_T(self, speed):
    #     self.motor3.speed(speed)

    def speed_LR(self, speed1, speed2):
        self.set_left_speed = abs(speed1)
        self.set_right_speed = abs(speed2)

        self.motor1.run(-speed1)
        self.motor2.run(speed2)

    def get_motor_feedback(self):

        left_speed = abs(self.motor1.speed())
        right_speed = abs(self.motor2.speed())

        left_load = abs(self.motor1.load())
        right_load = abs(self.motor2.load())

        return {
            "left": {
                "actual_speed": left_speed,
                "commanded_speed": self.set_left_speed,
                "load": left_load
            },

            "right": {
                "actual_speed": right_speed,
                "commanded_speed": self.set_right_speed,
                "load": right_load
            }
        }

    def stop_wheels(self):
        self.motor1.stop()
        self.motor2.stop()

        self.set_left_speed = 0
        self.set_right_speed = 0

    @staticmethod
    def current_speed(motor):
        return motor.speed()

    @staticmethod
    def hold_speed(motor):
        motor.hold()


class Wheel_Odometry:

    def __init__(self, motors):

        self.motors = motors

        self.wheel_diameter = MotorSettings.WHEEL_DIAMETER_MM
        self.wheel_spacing = MotorSettings.WHEEL_SPACING_MM

        self.mm_per_degree = (
            math.pi * self.wheel_diameter / 360
        )

        # Local encoder reference
        self.reference_left = self.motors.motor1.angle()
        self.reference_right = self.motors.motor2.angle()

    # ========================================
    # RELATIVE ROTATION
    # ========================================

    def get_relative_rotation(self):

        left_angle = self.motors.motor1.angle()
        right_angle = self.motors.motor2.angle()

        # Correct for opposing motor mounting
        left_change = -(
            left_angle - self.reference_left
        )

        right_change = (
            right_angle - self.reference_right
        )

        left_distance = (
            left_change * self.mm_per_degree
        )

        right_distance = (
            right_change * self.mm_per_degree
        )

        rotation = math.degrees(
            (right_distance - left_distance)
            / self.wheel_spacing
        )

        return rotation

    # ========================================
    # RESET REFERENCE
    # ========================================

    def reset_relative_rotation(self):

        self.reference_left = (
            self.motors.motor1.angle()
        )

        self.reference_right = (
            self.motors.motor2.angle()
        )

    # ========================================
    # TURN CALCULATIONS
    # ========================================

    def degree_to_wheel_rotation(self, angle):

        distance = (
            abs(angle) * math.pi * self.wheel_spacing
        ) / 360

        return (
            distance / (math.pi * self.wheel_diameter)
        ) * 360

    # ========================================
    # ENCODER-BASED TURN
    # ========================================

    async def turn_degree(
        self,
        degree,
        speed,
        acceleration
    ):

        if degree == 0:
            return

        wheel_rotation = (
            self.degree_to_wheel_rotation(degree)
        )

        direction = 1 if degree > 0 else -1

        left_target = (
            self.motors.motor1.angle()
            + direction * wheel_rotation
        )

        right_target = (
            self.motors.motor2.angle()
            + direction * wheel_rotation
        )

        left_limits = self.motors.motor1.control.limits()
        right_limits = self.motors.motor2.control.limits()

        try:

            self.motors.motor1.control.limits(
                abs(speed), abs(acceleration), 100
            )

            self.motors.motor2.control.limits(
                abs(speed), abs(acceleration), 100
            )

            self.motors.motor1.run_target(
                abs(speed) * direction,
                left_target,
                wait=False
            )

            self.motors.motor2.run_target(
                abs(speed) * direction,
                right_target,
                wait=False
            )

            while (
                not self.motors.motor1.done()
                or not self.motors.motor2.done()
            ):

                await wait(MotorSettings.TURN_LOOP_INTERVAL_MS)

        finally:

            self.motors.motor1.control.limits(*left_limits)
            self.motors.motor2.control.limits(*right_limits)

            # Hand the drive motors directly back to forward motion instead
            # of inserting a stopped interval after every turn.
            self.motors.speed_LR(speed, speed)

    # ========================================
    # TEST
    # ========================================

    async def test_relative_rotation(self):

        self.reset_relative_rotation()

        print("Relative rotation test started")

        while True:

            rotation = self.get_relative_rotation()

            print(
                "Relative rotation:",
                round(rotation, 2)
            )

            await wait(MotorSettings.POST_TURN_TEST_INTERVAL_MS)










