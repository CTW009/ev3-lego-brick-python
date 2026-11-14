from Motors import Motors
from pybricks.hubs import EV3Brick

motor = Motors()
ev3 = EV3Brick()
print("hi")
def main():
    while True:
        turn_right(800)


def move_forward():
    motor.speed_LR(800, 800)

def move_backward():
    motor.speed_LR(-800, -800)

def turn_left(speed):
    motor.speed_L(0)
    motor.speed_R(speed)

def turn_right(speed):
    motor.speed_R(0)
    motor.speed_L(speed)

def spin_radar():
    motor.speed_T(500)

main()