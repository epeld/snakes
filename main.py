import pygame, sys
from pygame.locals import *

import colors
import geometry
import time_utils
import game as gm
import graphics as gfx

def process_events(game):
    for event in pygame.event.get():
        if event.type==QUIT:
            game.set_done()


def main():
    pygame.init()

    game = gm.Game()
    display = gfx.create_display()
    while not game.get_done():
        process_events(game)
        pygame.display.update()

        pygame.time.wait(500)

    pygame.quit()
    sys.exit()


main()
