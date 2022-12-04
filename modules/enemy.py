import pygame
from .frect import FRect
from .entity import Entity
from enum import Enum
from .weapons import Projectile
import json
from .engine import *
from random import randint

class State(Enum):

    IDLE = 0
    FOLLOWING = 1
    ATTACKING = 2
    DEAD = 3

ENEMY_SHAPE = json.load(open("data/enemy_data/enemy_shape.json"))
ENEMY_STATS = json.load(open("data/enemy_data/enemy_stats.json"))

class Enemy(Entity):

    def __init__(self, master, grps, start_pos, shape_type, stats_type):

        super().__init__(grps)

        self.master = master
        self.screen = pygame.display.get_surface()

        self.type = stats_type
        self.sprite_hit_box_y_off = ENEMY_SHAPE[shape_type]["y_off"]
        self.start_pos = start_pos
        self.hitbox = FRect(*self.start_pos, *ENEMY_SHAPE[shape_type]["ground_size"])
        self.sprite_box = FRect(0, 0, *ENEMY_SHAPE[shape_type]["size"])

        self.image = pygame.image.load(F"graphics/enemies/{shape_type}.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.hitbox.midbottom))

        self.state = State.FOLLOWING
        self.direction = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = ENEMY_STATS[self.type]["speed"] + randint(-1, 1)/10
        self.moving = True
        self.invincible = False
        self.hurting = False

        self.kb_direction = pygame.Vector2(0, 0)
        self.kb_speed = 6

        self.damage = ENEMY_STATS[self.type]["damage"]
        self.health = ENEMY_STATS[self.type]["health"]

        self.HURT_DURATION_TIMER = CustomTimer()

        # self.EVENTS = ()

    def check_player_hit(self):

        if not self.master.player.invincible and self.sprite_box.colliderect(self.master.player.sprite_box):

            self.master.player.got_hit(self)

    def die(self):
        
        self.master.enemy_handler.enemies_killed += 1
        self.kill()

    def got_hit(self, power, kb_direction):

        if self.invincible: return

        self.health -= power
        if self.health <= 0:
            self.die()
            return
        self.kb_direction:pygame.Vector2 = kb_direction
        self.invincible = True
        self.hurting = True
        self.state = State.IDLE
        self.HURT_DURATION_TIMER.start(100)

    def process_events(self):
        
        # for event in pygame.event.get(self.EVENTS):
        if self.HURT_DURATION_TIMER.check():
            self.invincible = False
            self.hurting = False
            self.state = State.FOLLOWING
            self.velocity.update(0, 0)


    def update_image(self):

        # if self.hurting:
        #     self.image.fill((255,0,0), special_flags=pygame.BLEND_RGB_MULT)
        self.rect.midbottom = self.hitbox.midbottom

    def move(self):

        if self.state == State.FOLLOWING:
                self.direction = (self.master.player.sprite_box.center + pygame.Vector2(0, 0) - self.sprite_box.center).normalize()
                self.velocity = self.direction * self.max_speed

                for enemy in self.master.enemy_grp.sprites():
                    if enemy == self: continue
                    if self.sprite_box.colliderect(enemy.sprite_box):
                        try:
                            self.velocity += (self.sprite_box.center + pygame.Vector2(0, 0) - enemy.sprite_box.center).normalize()
                        except ValueError: pass
        elif self.hurting:
            self.velocity.update(self.kb_direction*self.kb_speed*self.master.dt)
        else:
            self.velocity.update(0, 0)

        self.hitbox.centerx += self.velocity.x * self.master.dt
        self.check_bounds_collision(0, self.master.level.bounds)
        self.hitbox.bottom += self.velocity.y * self.master.dt
        self.check_bounds_collision(1, self.master.level.bounds)

        self.sprite_box.centerx = self.hitbox.centerx
        self.sprite_box.bottom = self.hitbox.bottom - self.sprite_hit_box_y_off

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)

    def update(self):

        self.process_events()
        self.move()
        self.check_player_hit()
        self.update_image()


class RangedEnemy(Enemy):

    def __init__(self, master, grps, start_pos, shape_type, stats_type):
        super().__init__(master, grps, start_pos, shape_type, stats_type)

        self.attack_range = 100 + randint(-15, 15)
        self.can_attack = True

        self.ATTACK_DELAY_TIMER = CustomTimer()
        self.HALT_TIMER = CustomTimer()

        # self.SUB_EVENTS = (self.ATTACK_DELAY_TIMER, self.HALT_TIMER)

    def attack(self):
         
        proj = Projectile(self.master,
        [self.master.level.enemy_projectile_grp, self.master.level.y_sort_grp],
        "projectile_black", self.sprite_box.center, self.direction, 1, 15)

        proj.check_hit = proj.check_player_hit

    def process_events(self):

        super().process_events()


        if self.ATTACK_DELAY_TIMER.check():
            self.can_attack = True

        if self.HALT_TIMER.check():
            self.state = State.FOLLOWING

    def state_maneger(self):

        player = self.master.player
        if self.can_attack and ((self.sprite_box.centerx-player.sprite_box.centerx)**2 + (self.sprite_box.centery-player.sprite_box.centery)**2) < self.attack_range**2:
            self.can_attack = False
            self.attack()
            self.ATTACK_DELAY_TIMER.start(5_000)
            self.HALT_TIMER.start(1_500)
            self.state = State.ATTACKING

    def update(self):

        super().update()
        self.state_maneger()
        