from pybricks.ev3devices import Motor
from pybricks.parameters import Port

class Motors:
    def __init__(self):
        self.motor1 = Motor(Port.A)
        self.motor2 = Motor(Port.D)
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