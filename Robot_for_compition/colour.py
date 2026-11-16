from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color




class colour:

   """
   This class controls the three colour sensors on the robot.
   Each sensor can identify a colour and return a numerical
   value that can be used by the main program to decide
   what the robot should do.
   """

   def __init__(self):
       # Set up the three colour sensors using their EV3 ports.
       # Sensor 1 is at the front left of the robot.
       # Sensor 2 is at the front right of the robot.
       # Sensor 3 is located at the back of the robot.


       self.sensor_1 = ColorSensor(Port.S1)
       self.sensor_2 = ColorSensor(Port.S2)
       self.sensor_3 = ColorSensor(Port.S3)

   def detect_left(self):
        return self.detect_color(self.sensor_1)

   def detect_right(self):
        return self.detect_color(self.sensor_2)


   def detect_back(self):
        return self.detect_color(self.sensor_3)


   def detect_color(self, sensor):
       """
       :returns: 1 ,2, 3, 4, 5,
       -1 if no color detected
       """


       detected = sensor.color()


       # Check the detected colour and return its assigned value.
       if detected == Color.BLACK:
           return 1


       elif detected == Color.WHITE:
           return 0


       elif detected == Color.GREEN:
           return 2


       elif detected == Color.RED:
           return 3


       elif detected == Color.YELLOW:
           return 4


       elif detected == Color.BLUE:
           return 5


       # Return -1 if the sensor detects a colour
       # that is not included in the list above.
       else:
           return -1
