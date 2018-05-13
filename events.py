import pygame
from pygame.locals import *

def process_events(game):
    for event in pygame.event.get():
        if event.type==QUIT:
            game.set_done()
