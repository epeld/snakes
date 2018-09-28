import pygame, sys
import random
import math
from pygame.locals import *

WHITE=pygame.color.Color(255,255,255)
BLACK=pygame.color.Color(0,0,0)
TRANSPARENT_COLOR=pygame.color.Color(255,255,255, 0)
BACKGROUND_COLOR=WHITE

def darken(color):
    return pygame.color.Color(
        round(color.r * 0.5),
        round(color.g * 0.5),
        round(color.b * 0.5)
    )

def lighten(color):
    return pygame.color.Color(
        min(255, round(color.r * 1.5)),
        min(255, round(color.g * 1.5)),
        min(255, round(color.b * 1.5))
    )

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

class VaryingWormStateInterval(object):
    """A helper for keeping track of worm state. Toggles automatically between "on" and "off" with varying intervals"""
    def __init__(self):
        self.on = True
        self.length = self.randomize_length(self.on)

    def randomize_length(self, on):
        if on:
            return random.randint(50, 150)
        else:
            return random.randint(10, 15)

    def update(self):
        self.length -= 1
        if self.length <= 0:
            self.on = not self.on
            self.length = self.randomize_length(self.on)

    def is_on(self):
        return self.on


class Player(object):
    def __init__(self):
        self.reset()
        self.color = pygame.color.Color(100,200,250)
        self.state = VaryingWormStateInterval()

    def get_color(self):
        return self.color

    def get_head_color(self):
        return darken(self.color)

    def get_hole_color(self):
        return lighten(self.color)

    def is_hole(self):
        return not self.state.is_on()

    def update(self, speed):
        self.state.update()
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


class CountdownState(object):
    def __init__(self):
        self.started = False

    def did_finish(self, updated_time):
        return self.get_count(updated_time) == 0

    def start(self, start_time):
        self.started = True
        self.start_time = start_time

    def did_start(self):
        return self.started

    def get_count(self, updated_time):
        INITIAL_COUNT = 3
        if not self.started:
            return INITIAL_COUNT
        return max(0, INITIAL_COUNT - math.ceil((updated_time - self.start_time) / 1000))

def main():
    pygame.display.init()
    pygame.font.init()

    player = Player()
    players = [player]

    recent_rects = FifoQueue()

    # Set up display
    DEPTH=32
    DISPLAY=pygame.display.set_mode((640,480),0,DEPTH)
    TEMPORARY_RECTS=pygame.surface.Surface(DISPLAY.get_size(),SRCALPHA,DEPTH)
    BACKBUFFER=pygame.surface.Surface(DISPLAY.get_size(),SRCALPHA,DEPTH)
    COLLISION_MASK=pygame.surface.Surface(DISPLAY.get_size(),0,8)

    COLLISION_MASK.fill(WHITE)
    DISPLAY.fill(BACKGROUND_COLOR)
    BACKBUFFER.fill(BACKGROUND_COLOR)

    # Font stuff
    font = pygame.font.SysFont(next(f for f in pygame.font.get_fonts() if 'roman' in f), 50)
    game_over = font.render("HE DED.", True, BLACK)
    game_over_rt = game_over.get_rect()
    game_over_rt.center = DISPLAY.get_rect().center

    digits = [font.render(str(i), True, BLACK) for i in range(1, 4)]

    countdown = CountdownState()

    start_ticks = pygame.time.get_ticks()
    exit = False
    show_collision_mask = False
    while not exit:
        current_time = pygame.time.get_ticks()
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
                elif event.key == K_TAB:
                    show_collision_mask = not show_collision_mask
            elif event.type == KEYUP:
                player.stop_turning()

        for p in players:
            if not p.is_dead():
                player.update(speed=2)

        # Generate the new rectangles for each player
        rts = [p.rect(6) for p in players if not p.is_dead()]
        recent_rects.put(rts)

        # player rects older than 10 generations get
        # "persisted" to screen bitmap
        if recent_rects.size() > 10:
            oldest_player_rects = recent_rects.get()
            for rt in oldest_player_rects:
                if player.is_hole():
                    c = player.get_hole_color()
                else:
                    c = player.get_color()
                    COLLISION_MASK.fill(BLACK, rt)
                BACKBUFFER.fill(c, rt)

        # redraw overlay
        TEMPORARY_RECTS.fill(TRANSPARENT_COLOR)
        for generation in recent_rects.get_items():
            for rt in generation:
                c = player.get_head_color()
                TEMPORARY_RECTS.fill(c, rt)

        if show_collision_mask:
            DISPLAY.blit(COLLISION_MASK, (0,0))
        else:
            DISPLAY.blit(BACKBUFFER, (0,0))
        DISPLAY.blit(TEMPORARY_RECTS, (0,0))

        if all(p.is_dead() for p in players):
            DISPLAY.blit(game_over, game_over_rt.topleft)

        if not countdown.did_finish(current_time):
            countdown_loop(digits, TEMPORARY_RECTS, countdown)

        COLLISION_MASK.lock()
        for p in players:
            if p.is_dead():
                continue
            for pt in rect_corners(rt):
                x = int(pt[0])
                y = int(pt[1])
                color = COLLISION_MASK.get_at((x, y))
                if not are_same_color(color, WHITE):
                    BACKBUFFER.fill((250,0,0), (x, y, 3, 3))
                    p.set_dead(True)
        COLLISION_MASK.unlock()

        pygame.display.update()

        pygame.time.wait(10)


def countdown_loop(digits, background, countdown):
    DISPLAY = pygame.display.get_surface()
    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif not countdown.did_start():
                    countdown.start(current_time);

        if countdown.did_finish(current_time):
            return

        DISPLAY.fill(BACKGROUND_COLOR)
        DISPLAY.blit(background, (0,0))
        digit = digits[countdown.get_count(current_time) - 1]

        rt = digit.get_rect()
        rt.center = DISPLAY.get_rect().center

        DISPLAY.blit(digit, rt)
        pygame.display.update()

        pygame.time.wait(100)

main()

