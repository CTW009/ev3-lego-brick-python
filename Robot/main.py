import math
import pygame
import sys
import robot
import tools
#starting vars
W=tools.meter_to_pixel_converstion(4)
H=tools.meter_to_pixel_converstion(4)
#800px by 800px


#vars
stall_percentage=.9 #80% at what percentage will the robot detect its not moving
motor_target_percentage=1# minimum reading for motors to be at "target speed" ie target speed 600, minimum reading will be 540

class main:

    def __init__(self,screen_width,screen_height):
        pygame.init()

        # init classes
        self.robot_player = robot.robot(self)
        self.robot_player.init_connection_to_robot()
        self.watching_color = False


        #init vars

        #colours
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)


        #pygame controls

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("robot visualization 2D")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.speed_threshold_since = None
        self.last_stall_switch_at = pygame.time.get_ticks() - 1500

    def check_motor_stalling(self, motor_data):
        left_data = motor_data.get("A")
        right_data = motor_data.get("D")
        if (
            left_data is None
            or left_data.get("speed") is None
            or right_data is None
            or right_data.get("speed") is None
        ):
            return

        left_target = self.robot_player.left_motor_set_speed or 0
        right_target = self.robot_player.right_motor_set_speed or 0
        left_speed = left_data["speed"]
        right_speed = right_data["speed"]

        left_target_speed = abs(left_target) * motor_target_percentage
        right_target_speed = abs(right_target) * motor_target_percentage
        left_stall_limit = abs(left_target) * stall_percentage
        right_stall_limit = abs(right_target) * stall_percentage

        if self.robot_player.motor_change and (
            abs(left_speed) >= left_target_speed
            and abs(right_speed) >= right_target_speed
        ):
            self.robot_player.motor_change = False
            print("switched")

        left_commanded = left_target != 0
        right_commanded = right_target != 0
        left_low_speed = left_commanded and abs(left_speed) < left_stall_limit
        right_low_speed = right_commanded and abs(right_speed) < right_stall_limit
        left_reported_stalled = left_commanded and left_data.get("stalled", False)
        right_reported_stalled = right_commanded and right_data.get("stalled", False)

        low_speed_detected = left_low_speed or right_low_speed
        now = pygame.time.get_ticks()
        if low_speed_detected:
            if self.speed_threshold_since is None:
                self.speed_threshold_since = now
        else:
            self.speed_threshold_since = None

        low_speed_confirmed = (
            self.speed_threshold_since is not None
            and now - self.speed_threshold_since >= 1000
        )
        stalled_ports = []
        if left_reported_stalled or (low_speed_confirmed and left_low_speed):
            stalled_ports.append("A")
        if right_reported_stalled or (low_speed_confirmed and right_low_speed):
            stalled_ports.append("D")

        if stalled_ports and now - self.last_stall_switch_at >= 1500:
            print(
                "Stall detected on motor(s) {0}; switching motor direction".format(
                    ", ".join(stalled_ports)
                )
            )
            if left_commanded and right_commanded:
                self.robot_player.start_motors("A", -left_target)
                self.robot_player.start_motors("D", -right_target)
            if left_commanded:
                self.robot_player.start_motors("A", -left_target)
            if right_commanded:
                self.robot_player.start_motors("D", -right_target)
            self.last_stall_switch_at = now

    def front_wheels_up(self, motor_data):


#robot states

    def searching(self):
        pass
    def Attack(self):
        pass
    def flee(self):
        pass







if __name__ == '__main__':
    app = main(W, H)
    # Commands are sent once, outside the frame loop; sending them every frame
    # floods the PC-to-brick command queue.
    app.robot_player.start_motors("A", -600)
    app.robot_player.start_motors("D", 600)
    next_motor_read = pygame.time.get_ticks()
    next_data_report = next_motor_read
    running = True
    try:
        while running:

            #pygame loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            app.screen.fill(app.WHITE)

            if pygame.time.get_ticks() >= next_motor_read:
                app.robot_player.read_motor_data("all")
                next_motor_read = pygame.time.get_ticks() + 500

            for message in app.robot_player.update():
                print(message)
            motor_data = app.robot_player.get_motor_data()
            left_motor_data = motor_data.get("A")
            right_motor_data = motor_data.get("D")
            if left_motor_data is not None and left_motor_data.get("speed") is not None:
                app.robot_player.left_motor_speed = left_motor_data["speed"]
            if right_motor_data is not None and right_motor_data.get("speed") is not None:
                app.robot_player.right_motor_speed = right_motor_data["speed"]
            if pygame.time.get_ticks() >= next_data_report:
                print(motor_data)
                next_data_report = pygame.time.get_ticks() + 500

            app.check_motor_stalling(motor_data)

            # NEXT TO ADD IS USING LOAD WE CAN FIGURE OUT IF THE MOTORS ARE ON THE GROUND OR NOT
            #COLOR DETECTION
            #INTERUPTS FOR THE COLOR DETECTION BASED ON SURONDINGS
            #ATTACK MODE
            #SEARCH MODE
            #FLEE MODE
            #


            lines = []
            for port, values in motor_data.items():
                lines.append(
                    "{0}: angle={1} speed={2} load={3} stalled={4} done={5}".format(
                        port,
                        values["angle"],
                        values["speed"],
                        values["load"],
                        values["stalled"],
                        values["done"],
                    )
                )
            for row, line in enumerate(lines):
                text = app.font.render(line[:100], True, app.BLACK)
                app.screen.blit(text, (12, 12 + row * 24))

            pygame.draw.rect(app.screen, app.BLACK, app.robot_player.robotVisulization, 2)
            pygame.display.flip()
            app.clock.tick(60)
    finally:
        app.robot_player.close_connection()
        pygame.quit()

    sys.exit()
