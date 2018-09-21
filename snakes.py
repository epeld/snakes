import pygame, sys
import random
import math
from pygame.locals import *

WHITE=(255,255,255)

class Player(object):
    def __init__(self):
        self.pos = (50, 100)
        self.heading = 0

    def update(self, speed):
        dx = math.cos(self.heading) * speed
        dy = math.sin(self.heading) * speed
        x = self.pos[0] + dx
        y = self.pos[1] + dy
        self.pos = x, y
        return self.pos

    def rect(self, size):
        x = self.pos[0] - size/2
        y = self.pos[1] - size/2
        return (x, y, size, size)


def main():
    pygame.init()

    player = Player()
    
    # Set up display
    DISPLAY=pygame.display.set_mode((640,480),0,32)

    DISPLAY.fill(WHITE)

    start_ticks = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        player.update(5)
        player.heading = player.heading + 0.05
        pygame.draw.rect(DISPLAY,(100,200,250), player.rect(10))

        pygame.display.update()

        pygame.time.wait(50)


main()

