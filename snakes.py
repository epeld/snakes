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
    players = [player]

    recent_rects = FifoQueue()

    # Set up display
    DEPTH=32
    DISPLAY=pygame.display.set_mode((640,480),0,DEPTH)
    OVERLAY=pygame.surface.Surface(DISPLAY.get_size(),SRCALPHA,DEPTH)

    BACKGROUND_COLOR=WHITE
    DISPLAY.fill(BACKGROUND_COLOR)

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
                    DISPLAY.fill(BACKGROUND_COLOR)
                    player.reset()
                elif event.key == K_ESCAPE:
                    exit = True
            elif event.type == KEYUP:
                player.stop_turning()

        player.update(speed=2)

        # Generate the new rectangles for each player
        rts = [p.rect(10) for p in players]
        recent_rects.put(rts)

        # player rects older than 10 generations get
        # "persisted" to screen bitmap
        if recent_rects.size() > 10:
            oldest_player_rects = recent_rects.get()
            for rt in oldest_player_rects:
                pygame.draw.rect(DISPLAY,(100,200,250), rt)

        # redraw overlay
        OVERLAY.fill((255,255,255,0)) #transparent
        for generation in recent_rects.get_items():
            for rt in generation:
                pygame.draw.rect(OVERLAY,(200,100,50), rt)
        DISPLAY.blit(OVERLAY, (0,0))

        # DISPLAY.lock()
        # color = tuple(DISPLAY.get_at((int(rt[0]), int(rt[1]))))
        # if tuple(DISPLAY.get_at((int(rt[0]), int(rt[1])))) != BACKGROUND_COLOR:
        #     print("INTERSECT")
        #     print(color)
        # DISPLAY.unlock()

        pygame.display.update()

        pygame.time.wait(10)


main()

