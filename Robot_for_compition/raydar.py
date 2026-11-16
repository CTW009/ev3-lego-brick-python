from pybricks.parameters import Port
from pybricks.ev3devices import UltrasonicSensor

class RayDar:
    def __init__(self, motors):
        self.motors = motors #global
        self.raydar_motor = self.motors.motor3
        self.raydar = UltrasonicSensor(Port.S4)
        self.dict = {self.get_angle() : [self.raydar.distance(), self.raydar.presence()]}

        if self.raydar_motor.angle() >= 180:
            self.set_angle = 0
        else:
            self.set_angle = 360

    def rotate(self,speed=100):
        print("rotating")
        self.raydar_motor.run_angle(speed=speed, rotation_angle=self.set_angle, wait=False)

        if self.set_angle == 0:
            self.set_angle = 360
        if self.set_angle == 360:
            self.set_angle = 0

    def get_angle(self):
        return self.raydar_motor.angle()

    def update_dict(self):
        self.dict.update({self.get_angle() : [self.raydar.distance(), self.raydar.presence()]})
