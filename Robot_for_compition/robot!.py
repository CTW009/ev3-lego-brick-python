from Motors import Motors, Wheel_Odometry
from pybricks.hubs import EV3Brick


ev3 = EV3Brick()





class Robot:
    def __init__(self):
        self.motor = Motors() #put in varibles that we need to be global
        self.wheel_odometry = Wheel_Odometry(self.motor)







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
robot.wheel_odometry.turn_degree(360,500,300)
main()
