import pygame
from .config import *
from .engine import *
from .player import Player
from .enemy import Enemy, RangedEnemy
from .debug import Debug
from random import randint
import csv
from .object import Object
import os
from .ui import PlayerUI

class World:

    def __init__(self, master):

        self.master = master
        master.world = self

        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2(0,0)

        self.level = Level(master, 'test')

        self.debug = Debug()
        master.debug = self.debug

        self.whole_map = pygame.image.load("graphics/map/map.png").convert()

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

        self.screen.fill(0x949da8)
        self.screen.blit(self.whole_map, self.offset)
        self.level.draw()

    def update(self):
        
        self.update_offset()
        self.level.update()

class Level:

    def __init__(self, master, type) -> None:

        self.master = master
        master.level = self
        self.screen = pygame.display.get_surface()
        
        self.type = type
        self.bounds = self.load_bounds()
        # self.bounds = []

        self.y_sort_grp = YSortGroup()
        self.enemy_grp = pygame.sprite.Group()
        self.master.enemy_grp = self.enemy_grp
        self.enemy_projectile_grp = pygame.sprite.Group()

        self.player = Player(master, [self.y_sort_grp])
        self.player_ui = PlayerUI(master)

        self.enemy_spawner = EnemyHandler(master)

        self.mask_attack_grp = CustomGroup()

        self.load_objects()

    def load_objects(self):
        
        for file in os.listdir("data/object_data"):
            for pos in csv.reader(open(F"data/object_data/{file}")):
                Object(self.master, [self.y_sort_grp], file[:-4], [int(i) for i in pos])

    def load_bounds(self):

        bounds = []

        for bound in csv.reader(open(F"data/levels/{self.type}/bounds.csv")):

            rect = pygame.Rect(*[int(num) for num in bound])
            bounds.append(rect)

        return bounds

    def progress_stage(self, stage):

        pass

    def draw(self):

        # for rect in self.bounds:
        #     pygame.draw.rect(self.screen, "grey",
        #     (rect.x + self.master.world.offset.x, rect.y + self.master.world.offset.y, rect.width, rect.height))

        self.y_sort_grp.draw_y_sort(key=lambda sprite: sprite.hitbox.bottom)
        self.mask_attack_grp.draw()
        self.player_ui.draw()

    
    def update(self):

        self.player.update()
        self.enemy_grp.update()
        self.enemy_projectile_grp.update()
        self.enemy_spawner.update()
        self.mask_attack_grp.update()
        self.master.debug("count: ", len(self.enemy_grp))
        
class EnemyHandler:

    def __init__(self, master):

        self.master = master
        self.master.enemy_handler = self

        self.stage = 0 # 0-8 012-345-678  $%^&*()#123-456-789-10 [1-9]
        self.enemies_required = [8, 12, 16, 20, 26, 32, 40, 52] #[12, 16, 20, 26, 32, 40, 50, 64]
        # self.enemy_spawn_frq = [400,400,400,400,300,300,300,200,200]
        self.enemy_group_amount = [2,2,3,3,4,4,6,6,8]
        self.max_enemy_count = [16,16,16,22,22,22,28,28,28]
        self.enemies_killed = 0

        self.enemy_types = [
            {100:('Z', 'monster1', 'type1')},
            {80 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {70 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {60 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {60 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {60 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {60 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {60 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {60 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
            {60 :('Z', 'monster1', 'type1'), 100:('R', 'monster_r', 'type2')},
        ]

        self.ENEMY_SPAWNER_TIMER = pygame.event.custom_type()
        pygame.time.set_timer(self.ENEMY_SPAWNER_TIMER, 3_300)

        self.EVENTS = (self.ENEMY_SPAWNER_TIMER)

    def add_enemy(self, enemy_type, pos, enemy_sprite, enemy_stats):

        grps = (self.master.level.y_sort_grp, self.master.level.enemy_grp)

        if enemy_type == "Z": # zombie
            Enemy(self.master, grps, pos, enemy_sprite, enemy_stats)
        if enemy_type == "R": # ranged
            RangedEnemy(self.master, grps, pos, enemy_sprite, enemy_stats)

    def enemy_spawner(self):

        spawn_rects = (pygame.Rect(64,224,64,368), pygame.Rect(128,144,926,688), pygame.Rect(1056,192,112,544))

        while True:

            pos = randint(0, MAP_W), randint(0, MAP_H)
            rect = pygame.Rect(-self.master.world.offset.x, -self.master.world.offset.y, W, H)
            if not rect.collidepoint(pos):
                if any( [sp_rect.collidepoint(pos) for sp_rect in spawn_rects] ):
                    break

        rnd = randint(1, 100)
        possible_enemy:dict = self.enemy_types[self.stage]
        for num in sorted(possible_enemy.keys()):
            if num >= rnd:
                break
        type, sprite, stats = possible_enemy[num]

        for _ in range(self.enemy_group_amount[self.stage]):
            self.add_enemy(type, pos, sprite, stats)
        
    def process_events(self):

        for event in pygame.event.get(self.EVENTS):
            if event.type == self.ENEMY_SPAWNER_TIMER and len(self.master.level.enemy_grp) < self.max_enemy_count[self.stage]:
                self.enemy_spawner()

    def check_stage_progress(self):

        try:
            if self.enemies_killed >= self.enemies_required[self.stage]:
                self.stage += 1
                self.enemies_killed = 0
                self.master.level.progress_stage(self.stage)
        except IndexError: pass

    def update(self):

        self.process_events()
        self.check_stage_progress()
        self.master.debug("Stage: ", self.stage)