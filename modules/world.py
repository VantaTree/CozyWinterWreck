import pygame
from .debug import Debug
from .config import *

class World:

    def __init__(self, master):

        self.master = master
        master.world = self

        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2(0,0)

        self.debug = Debug()
        master.debug = self.debug

    def update_offset(self):
        # self.offset =  (self.master.player.hitbox.center - pygame.Vector2(W/2, H/2)) * -1
        camera_rigidness = 0.18 if self.master.player.moving else 0.05
        if self.master.player.dashing: camera_rigidness = 0.22
        self.offset -= (self.offset + (self.master.player.hitbox.center - pygame.Vector2(W/2, H/2))) * camera_rigidness * self.master.dt

    def draw_debug(self):
        self.debug.draw()

    def draw_foreground(self):
        pass

    def draw_background(self):

        self.screen.fill('lightgrey')

    def update(self):
        
        # self.update_offset()
        pass