
import pygame
import sys
import robot
import tools
#starting vars
W= tools.meter_to_pixel_converstion(4)
H=tools.meter_to_pixel_converstion(4)



class main:

    def __init__(self,screen_width,screen_height):
        # init classes
        self.robot_player = robot.robot(self)


        #init vars

        #colours
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)


        #pygame controls

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("robot visulization 2D")
        self.clock = pygame.time.Clock()
        pygame.init()




if __name__ == '__main__':
    main=main(W,H)
    # Game loop
    running = True

    while running:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background
        main.screen.fill(main.WHITE)

        # Draw something
        #pygame.draw.rect(screen, BLACK, (350, 250, 100, 100))

        # Update display
        pygame.display.flip()

        # Limit to 60 FPS
        main.clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()
