import pygame, sys
import colors
import geometry
from pygame.locals import *

SNAKE_WIDTH = 32 # The width of the snake body (in pixels)

def create_display():
    display = pygame.display.set_mode((640,480),0,32)
    display.fill(colors.WHITE)
    pygame.display.update()
    return display

def pygame_rect(rect):
    "Convert a geometry-rect to a pygame-Rect"
    return pygame.Rect(
        rect.get_top_left().to_tuple(),
        (rect.get_width(), rect.get_height())
    )

def draw_point(surface, pt, color):
    "Draw a snake position with a given color"
    rect = geometry.centered_square(pt, SNAKE_WIDTH)
    surface.fill(
        color,
        pygame_rect(rect)
    )

class GraphicsContext(object):
    "I represent a transparent bitmap and an API for drawing on top of that"

    def __init__(self, width, height, hardware=True):
        flags = SRCALPHA
        if hardware:
            flags |= HWSURFACE
        self.surface = pygame.Surface((width, height), flags)
        self.clear()

    def clear(self):
        "Clear the bitmap, making it fully transparent once more"
        self.surface.fill(colors.TRANSPARENT)

    def draw_point(self, pt, color):
        "Draw a snake position with a given color"
        rect = geometry.centered_square(pt, SNAKE_WIDTH)
        self.surface.fill(
            pygame_rect(rect),
            color
        )

    def blit(self, surface):
        "Blit the bitmap onto a destination surface"
        # TODO Idea:
        # track bounding box in draw_point so that
        # we can copy a smaller area
        pygame.surface.blit(
            self.surface,
            surface
        )
