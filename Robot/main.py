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
    speed_threshold_since = None
    stall_restart_active = False
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

            #speed vars
            left_speed = app.robot_player.left_motor_speed
            right_speed = app.robot_player.right_motor_speed
            left_target = app.robot_player.left_motor_set_speed
            right_target = app.robot_player.right_motor_set_speed

            # Track target-speed changes separately from ongoing stall detection.
            try:
                readings_ready = (
                    left_motor_data is not None
                    and left_motor_data.get("speed") is not None
                    and right_motor_data is not None
                    and right_motor_data.get("speed") is not None
                )
                if readings_ready:
                    left_target_speed = abs(left_target) * motor_target_percentage
                    right_target_speed = abs(right_target) * motor_target_percentage
                    left_stall_limit = abs(left_target) * stall_percentage
                    right_stall_limit = abs(right_target) * stall_percentage

                    if app.robot_player.motor_change and (
                        abs(left_speed) >= left_target_speed
                        and abs(right_speed) >= right_target_speed
                    ):
                        app.robot_player.motor_change = False
                        print("switched")

                    left_commanded = left_target != 0
                    right_commanded = right_target != 0
                    left_low_speed = left_commanded and abs(left_speed) < left_stall_limit
                    right_low_speed = right_commanded and abs(right_speed) < right_stall_limit
                    left_reported_stalled = left_commanded and left_motor_data.get("stalled", False)
                    right_reported_stalled = right_commanded and right_motor_data.get("stalled", False)

                    low_speed_detected = left_low_speed or right_low_speed
                    if low_speed_detected:
                        if speed_threshold_since is None:
                            speed_threshold_since = pygame.time.get_ticks()
                    else:
                        speed_threshold_since = None

                    low_speed_confirmed = (
                        speed_threshold_since is not None
                        and pygame.time.get_ticks() - speed_threshold_since >= 1000
                    )
                    stalled_ports = []
                    if left_reported_stalled or (low_speed_confirmed and left_low_speed):
                        stalled_ports.append(("A", left_target))
                    if right_reported_stalled or (low_speed_confirmed and right_low_speed):
                        stalled_ports.append(("D", right_target))

                    if stalled_ports and not stall_restart_active:
                        ports = ", ".join(port for port, _ in stalled_ports)
                        print(f"Stall detected on motor(s) {ports}; restarting at commanded speed")




                        #when a stall occurs this will be executed
                        app.robot_player.start_motors("A", app.robot_player.left_motor_set_speed*-1)
                        app.robot_player.start_motors("D", app.robot_player.right_motor_set_speed*-1)

                        stall_restart_active = True
                    elif not low_speed_detected and not left_reported_stalled and not right_reported_stalled:
                        stall_restart_active = False

            except Exception as exc:
                print(f"Motor check error: {exc}")

            # NEXT TO ADD IS USING LOAD WE CAN FIGURE OUT IF THE MOTORS ARE ON THE GROUND OR NOT




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
