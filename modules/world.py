import pygame
from .debug import Debug

class World:

    def __init__(self, master):

        self.master = master
        master.world = self

        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2(0,0)

        self.debug = Debug()
        master.debug = self.debug

    def update_offset(self):
        pass

    def draw_debug(self):
        self.debug.draw()

    def draw_foreground(self):
        pass

    def draw_background(self):

        self.screen.fill('cyan')

    def update(self):
        
        self.update_offset()