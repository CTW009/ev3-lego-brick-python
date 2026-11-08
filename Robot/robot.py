import pygame
import tools
class robot():


    def __init__(self,main_pointer):
        #this conversion is from meter to pixels put in real diminsions of robot
        self.width = tools.meter_to_pixel_converstion(.2)
        self.height = tools.meter_to_pixel_converstion(.2)

        self.x=100
        self.y=100

        self.robotVisulization=pygame.Rect(self.x,self.y,self.width,self.height)



    def update(self):
        pass