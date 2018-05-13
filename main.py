import pygame, sys
from pygame.locals import *
import random

import colors
import game as gm
import graphics as gfx
import geometry
import events
import simulation


def main():
    pygame.init()

    comms = simulation.SimulatedServerConnection()
    game = gm.Game()
    display = gfx.create_display()
    while not game.get_done():
        pending = events.process_events(game)
        comms.send_events(pending)

        updates = comms.receive_updates()
        if updates:
            for update in updates:
                pt = update.get_point()
                color = update.get_color()
                gfx.draw_point(display, pt, color)
            pygame.display.update()

        pygame.time.wait(50)

    pygame.quit()


main()
