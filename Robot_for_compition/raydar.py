from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.ev3devices import Motor, UltrasonicSensor


class RayDar:
    def __init__(self, motors):
        self.motors=motors #global
        self.raydar_motor = self.motors.motor3

        if self.raydar_motor.angle() >=180:
            self.set_angle=0
        else:
            self.set_angle=360


    def rotate(self,speed=100):
        print("rotating")
        self.raydar_motor.run_angle(speed=speed, rotation_angle=self.set_angle, wait=False)

        if self.set_angle==0:
            self.set_angle=360
        if self.set_angle==360:
            self.set_angle=0

    







if __name__ == "__main__":
    pass