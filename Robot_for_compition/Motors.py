from pybricks.ev3devices import Motor
from pybricks.parameters import Port
import math
class Motors:
    def __init__(self):
        self.motor1 = Motor(port=Port.A, gears=[12,20])
        self.motor2 = Motor(port=Port.D, gears=[12,20])
        #self.motor3 = Motor(Port.B)

    def speed_L(self, speed):
        self.motor1.run(-speed)

    def speed_R(self, speed):
        self.motor2.run(speed)

    #def speed_T(self, speed):
        #self.motor3.speed(speed)

    def speed_LR(self, speed1, speed2):
        self.motor1.run(-speed1)
        self.motor2.run(speed2)

    @staticmethod
    def current_speed(motor):
        return motor.speed()

    @staticmethod
    def hold_speed(motor):
        motor.hold_speed(0)



class Wheel_Odometry:

    def __init__(self,motors):
        self.motors=motors
        self.wheel_diameter = 53  # mm
        self.wheel_spaceing=145.6 # mm
        self.left_wheel_travel = 0  # this is the amount of distance one wheel will travel and is estamited
        self.right_wheel_travel = 0
        #inital, and final vars
        self.start_angle_L = 0
        self.start_angle_R = 0
        self.curent_angle_L = 0
        self.curent_angle_R = 0
        self.error_correction=.05 #amount of seconds that are to correct the time for the motors to speed up


    def degre_to_turn(self,angle):
        return (abs(angle)*self.wheel_spaceing)/self.wheel_diameter
        #M = |turn angle| × wheel spacing ÷ wheel diameter

    def calulate_turning_seconds(self,angle,speed,aceleration):
        degrees=self.degre_to_turn(angle)
        speed = abs(speed)
        aceleration = abs(aceleration)
        if speed == 0 or aceleration == 0:
            return -1
        # error handling

        if degrees >= math.pow(speed,2)/aceleration:
            # Accelerate to speed, cruise, then decelerate to a stop.
            return degrees/speed + speed/aceleration
        else:
            # Short turn: accelerate and decelerate without reaching max speed.
            return 2*math.sqrt(degrees/aceleration)

        #calc time






        """print(f"angle:{angle},speed:{speed}")
        return (abs(angle) *self.wheel_spaceing)/(self.wheel_diameter * speed)


         | turn angle | × wheel spacing
        ─────────────────────────────────────────
        wheel diameter × motor speed
        

        #gives us how much we need to rotate
        # """



    #TURNS AT CENTER OF ROBOT/center of rotation
    def turn_degree(self, degree,speed,aceleration):
        if degree == 0:
            print("invalid number passed")
            return

        self.start_angle_L = self.motors.motor1.angle()
        self.start_angle_R = self.motors.motor2.angle()
        #calc seconds for turn
        seconds=self.calulate_turning_seconds(degree,speed,aceleration)

        #error correction/proscessing
        if seconds == -1:
            print("invalid number passed")
            return
        seconds=seconds+self.error_correction

        reset_vals1=self.motors.motor1.control.limits()
        reset_vals2=self.motors.motor2.control.limits()

        #limits motors for a consitant actions
        self.motors.motor1.control.limits(abs(speed), abs(aceleration), 100)
        self.motors.motor2.control.limits(abs(speed), abs(aceleration), 100)

        #converting for run time in ms*
        ms=int(seconds*1000 + 0.5)
        #if turning left or right!

        # Positive degrees turn clockwise; negative degrees turn counterclockwise.
        # The left motor is mounted in the opposite direction to the right motor.
        motor_speed = -abs(speed) if degree > 0 else abs(speed)
        self.motors.motor1.run_time(motor_speed,ms,wait=False)
        self.motors.motor2.run_time(motor_speed,ms,wait=True)


        #reset limits to before turn
        self.motors.motor1.control.limits(reset_vals1[0],reset_vals1[1],reset_vals1[2])
        self.motors.motor2.control.limits(reset_vals2[0],reset_vals2[1],reset_vals2[2])














