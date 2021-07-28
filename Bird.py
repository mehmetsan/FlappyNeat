import pygame
import os

class Bird:
    """
    Bird class representing the flappy bird
    """
    MAX_ROTATION = 25
    IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join(os.getcwd(),"res","bird" + str(x) + ".png"))) for x in range(1,4)]
    ROT_VEL = 20
    ANIMATION_TIME = 5


    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        self.img = self.IMGS[0]
        self.img_count = 0

        self.x = x
        self.y = y

        # degrees to tilt
        self.tilt = 0           
        self.tick_count = 0
        self.vel = 0

        # second variable to store y value
        self.height = self.y 

    def jump(self):

        self.vel = -10.5
        self.height = self.y

        # Reset the ticks
        self.tick_count = 0

    def move(self):
 
        self.tick_count += 1
        # tried experimentaly
        gravity = 1.8           

        # Increasing acceleration
        acc = gravity *(self.tick_count)**2


        # for downward acceleration
        displacement = self.vel*(self.tick_count) + acc  

        # fall velocity control 
        THRESHOLD = 10

        if displacement >= THRESHOLD:
            displacement = (displacement/abs(displacement)) * 16

        # UPWARDS CHECK
        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt = self.tilt - self.ROT_VEL

    def draw(self, win):

        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # tilt the bird

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)  

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
