import pygame
from .player import Player
from .entity import SpriteGroup, YSortGroup
from .enemy import Enemy, RangedEnemy
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
        self.level.update()

class Level:

    def __init__(self, master, type) -> None:

        self.master = master
        self.screen = pygame.display.get_surface()
        
        self.type = type
        self.bounds = self.load_bounds()

        self.y_sort_grp = YSortGroup()
        self.enemy_grp = pygame.sprite.Group()
        self.master.enemy_grp = self.enemy_grp
        self.enemy_projectile_grp = pygame.sprite.Group()

        self.player = Player(master, [self.y_sort_grp])
        Enemy(master, [self.y_sort_grp, self.enemy_grp], (200, 100), "enemy1", "type1")
        RangedEnemy(master, [self.y_sort_grp, self.enemy_grp], (120, 220), "enemy2", "type2")
        RangedEnemy(master, [self.y_sort_grp, self.enemy_grp], (120, 240), "enemy2", "type2")
        RangedEnemy(master, [self.y_sort_grp, self.enemy_grp], (140, 200), "enemy2", "type2")
        RangedEnemy(master, [self.y_sort_grp, self.enemy_grp], (160, 200), "enemy2", "type2")
        RangedEnemy(master, [self.y_sort_grp, self.enemy_grp], (140, 240), "enemy2", "type2")

    def load_bounds(self):

        bounds = []

        for y, line in enumerate(csv.reader(open(F"data/levels/{self.type}/bounds.csv"))):
            for x, cell in enumerate(line):
                if cell == '1':
                    rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                    bounds.append(rect)
        return bounds

    def draw(self):

        for rect in self.bounds:
            pygame.draw.rect(self.screen, "grey",
            (rect.x + self.master.world.offset.x, rect.y + self.master.world.offset.y, rect.width, rect.height))

        self.y_sort_grp.draw_y_sort(key=lambda sprite: sprite.hitbox.bottom)

    
    def update(self):

        self.player.update()
        self.enemy_grp.update()
        self.enemy_projectile_grp.update()
        
