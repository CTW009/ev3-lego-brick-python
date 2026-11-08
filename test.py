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

while True:
    ev3.screen.print("Color:", detected_color)
    ev3.screen.print("Done!")
    ev3.speaker.beep(1000)
    wait(500)
    ev3.screen.clear()
    
    
    
    I am developing a LEGO Mindstorms EV3 robot using Pybricks MicroPython and the pybricks-cli package.

I want you to implement a reliable bidirectional communication system between my computer and my EV3 brick.

IMPORTANT EXISTING SETUP:
- The robot uses an EV3 brick running Pybricks MicroPython.
- I use pybricks-cli, invoked through the "pb" command, to run programs on the EV3.
- My computer runs regular Python inside a virtual environment.
- I have successfully connected to the EV3 over Bluetooth.
- I have previously used the color sensor and seen output such as "color.red" in the terminal when running main.py.
- The EV3 can run only one main program at a time.
- The computer will run the radar visualization, mapping, obstacle tracking, and high-level decision-making.
- The EV3 will handle hardware access, sensor polling, and local motor control.

PROJECT OBJECTIVE:
Create a reusable communication layer that allows my computer to:
1. Launch the EV3's main.py using pybricks-cli.
2. Receive continuous sensor data printed by the EV3.
3. Send commands to the EV3 while the program is running.
4. Parse incoming messages into structured Python data.
5. Allow other Python modules to access the latest sensor readings.
6. Shut down the EV3 program safely.

ARCHITECTURE:
Separate the implementation into two sides.

COMPUTER SIDE:
Create a Python module called ev3_communication.py.

It should provide a class called EV3Communication with:
- connect()
- disconnect()
- send_command()
- get_latest_sensor_data()
- is_connected()
- register_sensor_callback()

Use subprocess to launch the pb command. Do not assume that pb supports stdin or stdout piping without verifying it. Inspect the installed CLI's help and, if needed, its installed documentation or source code to establish the correct supported input/output mechanism.

The communication system must support simultaneous receiving and sending. Use appropriate threads or asynchronous I/O so receiving output never blocks the ability to send commands.

Use a thread-safe queue or equivalent for incoming messages. Make sure other modules can safely retrieve the latest sensor values.

EV3 SIDE:
Create a single main.py file for the EV3. All hardware imports and hardware initialization must occur on the EV3, not on my computer.

The EV3 program should:
- Initialize the EV3 brick and motors.
- Continuously read available sensors.
- Send sensor data to the computer.
- Receive and process commands without blocking sensor polling.
- Execute motor commands locally.
- Stop motors safely if communication is lost or a timeout occurs.

HARDWARE:
- Two EV3 color sensors, positioned above the left and right wheels, used to detect the black tape boundaries of the playing field.
- One EV3 ultrasonic sensor, used to detect other moving robots.
- One EV3 gyro sensor, used for heading and rotation measurements.
- Two drive motors.
- The radar sensor is mounted on a rotating mechanism. Verify which motor/port is assigned to it before assuming a third motor exists. My current listed hardware has two motors, so do not invent an additional motor or port.

MESSAGE PROTOCOL:
Use a simple, reliable protocol. Prefer newline-delimited JSON if supported by the communication channel.

Example sensor message:
{"type":"sensor_data","gyro":45.2,"left_color":12,"right_color":14,"ultrasonic":35}

Example motor command:
{"type":"motor_command","left_speed":200,"right_speed":200}

Also support:
- STOP
- FORWARD
- BACKWARD
- SET_SPEED
- GET_SENSORS
- SHUTDOWN

Validate incoming commands and handle malformed messages without crashing.

IMPORTANT TECHNICAL REQUIREMENTS:
- Do not use input() in the main sensor polling loop because it blocks execution.
- Do not assume subprocess stdin works with pb run. Verify it first.
- Do not create a second Bluetooth connection if the existing pb session already supports bidirectional communication.
- Do not use Pybricks hardware libraries in the computer-side virtual environment.
- Do not invent APIs or assume undocumented pybricks-cli capabilities.
- Avoid unnecessary dependencies.
- Keep the EV3 program lightweight.
- Include communication error handling.
- Include a safe motor stop on shutdown.
- Use a reasonable sensor reporting frequency that the EV3 can maintain.
- Keep the communication protocol extensible so I can add radar and mapping data later.

PROJECT STRUCTURE:
I want the following structure on my computer:

EV3_Radar/
    main.py
    ev3_communication.py
    config.py
    radar/
    mapping/
    robot/
    visualization/

The EV3 main.py should be uploaded/run through the CLI, while the other files stay on my computer.

DEVELOPMENT PROCESS:
Before writing code:
1. Inspect my installed pybricks-cli version.
2. Inspect the available pb commands and their options.
3. Establish how the CLI transports program input and output.
4. Determine whether bidirectional communication is supported in a single pb run session.
5. Explain any limitations before implementing a workaround.

Then:
1. Implement the smallest working communication test.
2. Verify that the computer receives EV3 messages.
3. Verify that the EV3 receives computer commands.
4. Add continuous sensor reporting.
5. Add motor command handling.
6. Add safe shutdown and connection-loss handling.

DELIVERABLES:
- Complete computer-side Python code.
- Complete EV3-side MicroPython code.
- Installation commands for any required dependencies.
- Exact commands to run and upload the EV3 program.
- A test procedure for sending STOP, FORWARD, and sensor requests.
- An explanation of how other modules can access the communication class.
- Clear instructions for activating my existing virtual environment.

Do not give me pseudocode or incomplete placeholders as the final result. Produce working code based on the actual installed CLI capabilities. If something cannot be verified, clearly explain it rather than guessing.

Prioritize reliability, modularity, and compatibility with my existing setup.