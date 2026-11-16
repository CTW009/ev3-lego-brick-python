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

   async def detect_left(self):
       return await self.detect_color(self.sensor_1)

   async def detect_right(self):
       return await self.detect_color(self.sensor_2)

   async def detect_back(self):
       return await self.detect_color(self.sensor_3)

   async def detect_color(self, sensor):

       # Read the sensor asynchronously.
       detected = await sensor.color()

       print("Detected:", detected)

       # Convert detected colour into a numerical value.
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

       else:
           return -1
