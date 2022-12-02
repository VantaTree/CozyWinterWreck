import pygame
from .debug import Debug
from .config import *
import csv

class World:

    def __init__(self, master):

        self.master = master
        master.world = self

        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2(0,0)

        self.level = Level(master, 'test')
        self.master.level = self.level

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
        self.level.draw()

    def update(self):
        
        self.update_offset()
        pass

class Level:

    def __init__(self, master, type) -> None:

        self.master = master
        self.screen = pygame.display.get_surface()
        
        self.type = type
        self.bounds = self.load_bounds()

    def load_bounds(self):

        bounds = []

        for y, line in enumerate(csv.reader(open(F"data/{self.type}/bounds.csv"))):
            for x, cell in enumerate(line):
                if cell == '1':
                    rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                    bounds.append(rect)
        return bounds

    def draw(self):

        for rect in self.bounds:
            pygame.draw.rect(self.screen, "grey",
            (rect.x + self.master.world.offset.x, rect.y + self.master.world.offset.y, rect.width, rect.height))
        
