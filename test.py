from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.tools import wait

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize motors


# Initialize a color sensor on Port 1
color_sensor = ColorSensor(Port.S1)

# Display a welcome message
ev3.screen.clear()
ev3.screen.print("Pybricks EV3 Starter")

# Play a beep sound
ev3.speaker.beep()

# Read color sensor value
detected_color = color_sensor.color()

# Display detected color
ev3.screen.clear()
ev3.screen.print("Color:", detected_color)

# End program
ev3.screen.print("Done!")