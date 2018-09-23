import pygame, sys
import random
import math
from pygame.locals import *

WHITE=pygame.color.Color(255,255,255)
TRANSPARENT_COLOR=pygame.color.Color(255,255,255, 0)


def are_same_color(c1, c2):
    return c1.r == c2.r and c1.g == c2.g and c1.b == c2.b

def rect_corners(rect):
    x, y, w, h = rect
    return [
        (x, y),
        (x + w, y),
        (x, y + h),
        (x + w, y + h)
    ]

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

    def is_dead(self):
        return self.dead

    def set_dead(self, b):
        self.dead = b

    def reset(self):
        self.dead = False
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
    pygame.display.init()

    player = Player()
    players = [player]

    recent_rects = FifoQueue()

    # Set up display
    DEPTH=32
    DISPLAY=pygame.display.set_mode((640,480),0,DEPTH)
    COMMITTED_RECTS=pygame.surface.Surface(DISPLAY.get_size(),SRCALPHA,DEPTH)
    TEMPORARY_RECTS=pygame.surface.Surface(DISPLAY.get_size(),SRCALPHA,DEPTH)

    BACKGROUND_COLOR=WHITE
    DISPLAY.fill(BACKGROUND_COLOR)
    COMMITTED_RECTS.fill(TRANSPARENT_COLOR)

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

        for p in players:
            if not p.is_dead():
                player.update(speed=2)

        # Generate the new rectangles for each player
        rts = [p.rect(8) for p in players if not p.is_dead()]
        recent_rects.put(rts)

        # player rects older than 10 generations get
        # "persisted" to screen bitmap
        if recent_rects.size() > 10:
            oldest_player_rects = recent_rects.get()
            for rt in oldest_player_rects:
                pygame.draw.rect(COMMITTED_RECTS,(100,200,250), rt)

        # redraw overlay
        TEMPORARY_RECTS.fill(TRANSPARENT_COLOR)
        for generation in recent_rects.get_items():
            for rt in generation:
                pygame.draw.rect(TEMPORARY_RECTS,(200,100,50), rt)

        DISPLAY.blit(COMMITTED_RECTS, (0,0))
        DISPLAY.blit(TEMPORARY_RECTS, (0,0))

        COMMITTED_RECTS.lock()
        for p in players:
            if p.is_dead():
                continue
            for pt in rect_corners(rt):
                x = int(pt[0])
                y = int(pt[1])
                color = COMMITTED_RECTS.get_at((x, y))
                if not are_same_color(color, TRANSPARENT_COLOR):
                    print(color)
                    print(TRANSPARENT_COLOR)
                    pygame.draw.rect(COMMITTED_RECTS,(250,0,0), (x,y, 3, 3))
                    p.set_dead(True)
                    print("DEAD")
        COMMITTED_RECTS.unlock()

        pygame.display.update()

        pygame.time.wait(10)


main()

