import pygame
import os

class Floor:
    
    VEL = 5
    WIDTH = pygame.transform.scale2x(pygame.image.load(os.path.join(os.getcwd(),"res","floor.png"))).get_width()
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(os.getcwd(),"res","floor.png")))

    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):

        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

