import pygame, sys
import random
import math
from pygame.locals import *

WHITE=(255,255,255)

class Player(object):
    def __init__(self):
        self.reset()

    def update(self, speed):
        dx = math.cos(self.heading) * speed
        dy = math.sin(self.heading) * speed
        x = self.pos[0] + dx
        y = self.pos[1] + dy
        self.pos = x, y

        if self.turning:
            if self.turning == 'LEFT':
                self.heading -= 0.05
            elif self.turning == 'RIGHT':
                self.heading += 0.05
        return self.pos

    def rect(self, size):
        x = self.pos[0] - size/2
        y = self.pos[1] - size/2
        return (x, y, size, size)

    def turn_left(self):
        self.turning = 'LEFT'

    def turn_right(self):
        self.turning = 'RIGHT'

    def stop_turning(self):
        self.turning = None


    def reset(self):
        self.pos = (50, 100)
        self.heading = 0
        self.turning = None


class FifoQueue(object):
    def __init__(self):
        self.items = []

    def put(self, item):
        self.items.append(item)

    def get(self):
        item = self.items[0]
        self.items = self.items[1:]
        return item

    def size(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items)

    def get_items(self):
        return self.items


def main():
    pygame.init()

    player = Player()
    
    # Set up display
    DISPLAY=pygame.display.set_mode((640,480),0,32)

    DISPLAY.fill(WHITE)

    start_ticks = pygame.time.get_ticks()
    exit = False
    while not exit:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.turn_left()
                elif event.key == K_RIGHT:
                    player.turn_right()
                elif event.key == K_SPACE:
                    DISPLAY.fill(WHITE)
                    player.reset()
                elif event.key == K_ESCAPE:
                    exit = True
            elif event.type == KEYUP:
                player.stop_turning()

        player.update(2)
        #player.heading = player.heading + 0.05
        pygame.draw.rect(DISPLAY,(100,200,250), player.rect(10))

        pygame.display.update()

        pygame.time.wait(10)


main()

