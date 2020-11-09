import pygame
import random
import os
import time
import neat
import pickle
pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("res","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("res","background.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("res","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("res","base.png")).convert_alpha())

class Bird():

    BIRDS = bird_frames
    GRAVITY = 5

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        self.x = x
        self.y = y
        self.tilt = 0           # degrees to tilt
        self.tick_count = 0     # every tick without a jump
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.BIRDS[0]

    def jump( self ):
        self.vel = -10
        self.y -= 10

    def move(self):
        """
        make the bird move
        :return: None
        """
        self.tick_count += 1

        # for downward acceleration
        displacement = self.vel*(self.tick_count) + GRAVITY * (self.tick_count)**2  # calculate displacement

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw( self , x , y , win ):

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)

class Pipe():



    GAP = 300
    VELOCITY = 5
    PIPE_HEIGHTS = [400, 600, 800]


    def __init__(self, x):

        self.x = x
        self.vel = VELOCITY
        self.height = 0
        self.active = True

        # where the top and bottom of the pipe is
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False

        self.set_height()

    def set_height(self):
        self.height = random.choice( PIPE_HEIGHTS )
        self.top    = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x = self.x - self.vel

    def draw(self, win):

        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
 
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bot_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask,top_offset)

        if bot_point or bot_point:
            return True

        return False

class Floor():


    VELOCITY = 5
    IMAGE = base_img
    WIDTH = IMAGE.get_width()

    def __init__(self, y):
        self.y = y
        self.leftX = 0
        self.rightX = self.WIDTH
        self.vel = VELOCITY

    def move():
        # Move the two base images

        self.rightX = self.rightX - self.vel
        self.leftx  = self.leftx - self.vel

        if(self.leftX < -self.WIDTH):
            self.leftX = self.WIDTH
        
        if(self.rightX < -self.WIDTH):
            self.rightX = self.WIDTH

    def draw(self, win):
        win.blit(self.IMAGE, (self.x1, self.y))
        win.blit(self.IMAGE, (self.x2, self.y))

