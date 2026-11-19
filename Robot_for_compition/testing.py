from pybricks.ev3devices import UltrasonicSensor
from settings import Hardware
from pybricks.tools import wait

def main():

    sensor = UltrasonicSensor(Hardware.ULTRASONIC_PORT)

    while True:

        distance = sensor.distance()

        print("Distance:", distance)

if __name__ == '__main__':
    main()