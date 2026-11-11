"""Pygame robot model and PC-to-EV3 command/response interface."""

import pygame
import tools
import pc_controller


class robot:
    def __init__(self, main_pointer, hub_name=pc_controller.DEFAULT_HUB_NAME):
        self.main_pointer = main_pointer
        self.width = tools.meter_to_pixel_converstion(0.2)
        self.height = tools.meter_to_pixel_converstion(0.2)
        self.x = 350
        self.y = 350
        self.robotVisulization = pygame.Rect(self.x, self.y, self.width, self.height)

        self.hub_name = hub_name
        self.connection = None
        self.received_messages = []
        self.motor_data = {}
        #in degrees per second
        self.left_motor_speed=0
        self.right_motor_speed=0
        self.left_motor_set_speed=0
        self.right_motor_set_speed=0
        self.motor_change=False#has the motor recntly changed, only goes back to false when set speed has been reached
    @property
    def connection_status(self):
        if self.connection is None:
            return "disconnected"
        return self.connection.status

    @property
    def connected(self):
        return self.connection is not None and self.connection.connected

    def init_connection_to_robot(self):
        if self.connection is not None and not self.connection.finished:
            return

        if self.connection is not None:
            self.received_messages.extend(self.connection.receive_messages())
            if self.connection.error:
                error_message = "Connection error: {0}".format(self.connection.error)
                if error_message not in self.received_messages:
                    self.received_messages.append(error_message)
            self.received_messages = self.received_messages[-100:]

        self.connection = pc_controller.PybricksSession(self.hub_name)
        self.connection.start()

    def send_to_robot(self, command):
        """Queue one brick command, such as ``rotate B 360`` or ``read all``."""
        if self.connection is None:
            self.init_connection_to_robot()
        try:
            self.connection.send_command(command)
        except RuntimeError:
            if not self.connection.finished:
                raise
            self.init_connection_to_robot()
            try:
                self.connection.send_command(command)
            except RuntimeError as error:
                if not self.connection.finished:
                    raise
                message = self.connection.error or str(error)
                self.received_messages.append("Command not sent: {0}".format(message))
                self.received_messages = self.received_messages[-100:]

    def read_motor_data(self, port="all"):
        self.send_to_robot("read {0}".format(port))

    def get_motor_data(self):
        """Return the latest motor readings, indexed by port letter."""
        return {port: values.copy() for port, values in self.motor_data.items()}

    def read_color_sensor(self):
        self.send_to_robot("color")

    def watch_color_sensor(self, interval_ms=250):
        self.send_to_robot("watch color {0}".format(int(interval_ms)))

    def stop_watching_color(self):
        self.send_to_robot("unwatch")

    def receive_from_robot(self):
        """Return newly received output lines from the EV3."""
        if self.connection is None:
            return []

        messages = []
        for line in self.connection.receive_messages():
            if line.startswith("MOTOR|"):
                fields = line.split("|")
                if len(fields) == 7:
                    try:
                        _, port, angle, speed, load, stalled, done = fields
                        self.motor_data[port] = {
                            "angle": int(angle),
                            "speed": int(speed),
                            "load": int(load),
                            "stalled": bool(int(stalled)),
                            "done": bool(int(done)),
                        }
                        continue
                    except ValueError:
                        pass
            messages.append(line)

        self.received_messages.extend(messages)
        self.received_messages = self.received_messages[-100:]
        return messages

    #comands!

    def start_motors(self, port,speed):
        #port-a,b,c,d
        #speed-degrees per second
        port = port.upper()

        self.send_to_robot(f"stop {port}")
        if port == "A":
            self.left_motor_set_speed = speed
            self.motor_change = True
        if port ==("D"):
            self.right_motor_set_speed = speed
            self.motor_change = True
        self.send_to_robot(f"start {port} {speed}")












    def update(self):
        """Poll incoming EV3 output; call this from the Pygame loop."""
        return self.receive_from_robot()

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None




