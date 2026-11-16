from Motors import Motors, Wheel_Odometry
from raydar import RayDar

from pybricks.hubs import EV3Brick


ev3 = EV3Brick()


class states:

    def __init__(self):

        self.Launching = False
        self.searching=False
        self.attack=False
        self.fleeing=False
        self.color_objective=False
        self.locked = False
        self.locked_process=None

    def set_state(self,state):
        if self.set_locked:
            pass
        else:
            self.set_locked = True
            self.locked_process = state

            if state == "launching":
                self.Launching = True
            if state == "searching":
                self.searching = True
            if state == "attacking":
                self.attack= True
            if state == "fleeing":
                self.fleeing = True
            if state == "color_objective":
                self.color_objective = True








    def set_state(self,state,overide):

        self.set_locked = True
        self.locked_process = state

        self.Launching = False
        self.searching = False
        self.attack=False
        self.fleeing = False
        self.color_objective = False


        if state == "launching":
            self.Launching = True
        if state == "searching":
            self.searching = True
        if state == "attacking":
            self.attack = True
        if state == "fleeing":
            self.fleeing = True
        if state == "color_objective":
            self.color_objective = True




    def read_state(self):
        return self.locked_process

    def set_lock(self,process_locked):
        if self.locked:
            return False
        else:
            self.locked = process_locked
            self.locked_process = process_locked
            return True





    def is_launching(self):
        return self.Launching
    def is_searching(self):
        return self.searching
    def is_attacking(self):
        return self.attack
    def is_fleeing(self):
        return self.fleeing
    def is_color_objective(self):
        return self.color_objective













class Robot:
    def __init__(self):
        self.motor = Motors() #put in varibles that we need to be global
        self.wheel_odometry = Wheel_Odometry(self.motor)
        self.raydar = RayDar(self.motor)






def main():
    while True:
        pass



def move_forward():
    robot.motor.speed_LR(800, 800)

def move_backward():
    robot.motor.speed_LR(-800, -800)

def turn_left(speed):
    robot.motor.speed_L(0)
    robot.motor.speed_R(speed)

def turn_right(speed):
    robot.motor.speed_R(0)
    robot.motor.speed_L(speed)



robot = Robot()
robot.wheel_odometry.turn_degree(180,500,300)
robot.raydar.rotate()
main()
