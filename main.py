import pygame, sys
import random
from pygame.locals import *
import simulation

WHITE=(255,255,255)

def main():
    pygame.init()

    # Set up display
    DISPLAY=pygame.display.set_mode((640,480),0,32)

    DISPLAY.fill(WHITE)

    # Set up event queue
    events = []

    simulation.setup()
    start_ticks = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        #
        # This is a simulation-snippet
        #
        elapsed = pygame.time.get_ticks() - start_ticks
        for event in simulation.get_events(elapsed):
            (_ms,x,y,w,h,color) = event
            pygame.draw.rect(DISPLAY,color,(x,y,w,h))
        #
        # End of simulation-snippet
        #

        pygame.display.update()

        pygame.time.wait(500)


main()
