import pygame
from .frect import FRect
from .entity import Entity
from enum import Enum
import json

class State(Enum):

    IDLE = 0
    FOLLOWING = 1
    ATTACKING = 2
    DEAD = 3

ENEMY_SHAPE = json.load(open("data/enemy_data/enemy_shape.json"))
ENEMY_STATS = json.load(open("data/enemy_data/enemy_stats.json"))

class Enemy(Entity):

    def __init__(self, master, grps, start_pos, shape_type, stats_type):

        for grp in grps:
            grp.add(self)

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
        self.max_speed = ENEMY_STATS[self.type]["speed"]
        self.acceleration = ENEMY_STATS[self.type]["acceleration"]
        self.deceleration = ENEMY_STATS[self.type]["deceleration"]
        self.moving = True

        self.damage = ENEMY_STATS[self.type]["damage"]

    def check_player_hit(self):

        if self.sprite_box.colliderect(self.master.player.sprite_box) and not self.master.player.invincible:

            self.master.player.got_hit(self)


    def update_image(self):

        self.rect.midbottom = self.hitbox.midbottom

    def move(self):

        if self.state == State.FOLLOWING:
                self.direction = (self.master.player.sprite_box.center + pygame.Vector2(0, 0) - self.sprite_box.center).normalize()
                self.velocity += self.direction * self.acceleration  * self.master.dt

                for enemy in self.master.enemy_grp.sprites:
                    if self.sprite_box.colliderect(enemy.sprite_box):
                        try:
                            self.velocity += (self.sprite_box.center + pygame.Vector2(0, 0) - enemy.sprite_box.center).normalize()
                        except ValueError: pass

        else:
            if self.velocity.magnitude_squared() >= self.deceleration**2:
                self.velocity -= self.velocity.normalize() * self.deceleration  * self.master.dt
            else: self.velocity.update(0, 0)

        if (mag:=self.velocity.magnitude_squared()):
            if mag > self.max_speed**2:
                    self.velocity.scale_to_length(self.max_speed)

        self.hitbox.centerx += self.velocity.x * self.master.dt
        self.check_bounds_collision(0, self.master.level.bounds)
        self.hitbox.bottom += self.velocity.y * self.master.dt
        self.check_bounds_collision(1, self.master.level.bounds)

        self.sprite_box.centerx = self.hitbox.centerx
        self.sprite_box.bottom = self.hitbox.bottom - self.sprite_hit_box_y_off

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)

    def update(self):

        self.move()
        self.check_player_hit()
        self.update_image()