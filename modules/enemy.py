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
        self.max_speed = ENEMY_STATS[self.type]["speed"]
        self.acceleration = ENEMY_STATS[self.type]["acceleration"]
        self.deceleration = ENEMY_STATS[self.type]["deceleration"]
        self.moving = True

        self.damage = ENEMY_STATS[self.type]["damage"]

        self.EVENTS = ()

    def check_player_hit(self):

        if not self.master.player.invincible and self.sprite_box.colliderect(self.master.player.sprite_box):

            self.master.player.got_hit(self)

    def process_events(self):
        pass

    def update_image(self):

        self.rect.midbottom = self.hitbox.midbottom

    def move(self):

        if self.state == State.FOLLOWING:
                self.direction = (self.master.player.sprite_box.center + pygame.Vector2(0, 0) - self.sprite_box.center).normalize()
                self.velocity += self.direction * self.acceleration  * self.master.dt

                for enemy in self.master.enemy_grp.sprites():
                    if enemy == self: continue
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

        self.process_events()
        self.move()
        self.check_player_hit()
        self.update_image()

class RangedEnemy(Enemy):

    def __init__(self, master, grps, start_pos, shape_type, stats_type):
        super().__init__(master, grps, start_pos, shape_type, stats_type)

        self.projec_image = pygame.image.load("graphics/test/projectile.png").convert_alpha()
        self.attack_range = 100
        self.can_attack = True

        self.ATTACK_DELAY_TIMER = pygame.event.custom_type()
        self.HALT_TIMER = pygame.event.custom_type()

        self.SUB_EVENTS = (self.ATTACK_DELAY_TIMER, self.HALT_TIMER)

    def attack(self):
         
        Projectile(self.master,
        [self.master.level.enemy_projectile_grp, self.master.level.y_sort_grp],
        self.projec_image, self.sprite_box.center, self.direction)
        

    def process_events(self):

        super().process_events()

        for event in pygame.event.get(self.SUB_EVENTS):

            if event.type == self.ATTACK_DELAY_TIMER:
                self.can_attack = True

            if event.type == self.HALT_TIMER:
                self.state = State.FOLLOWING

    def state_maneger(self):

        player = self.master.player
        if self.can_attack and ((self.sprite_box.centerx-player.sprite_box.centerx)**2 + (self.sprite_box.centery-player.sprite_box.centery)**2) < self.attack_range**2:
            self.can_attack = False
            self.attack()
            pygame.time.set_timer(self.ATTACK_DELAY_TIMER, 5_000, loops=1)
            pygame.time.set_timer(self.HALT_TIMER, 1_500, loops=1)
            self.state = State.ATTACKING

    def update(self):

        super().update()
        self.state_maneger()


class Projectile(pygame.sprite.Sprite):

    def __init__(self, master, grps, image, pos, direction):

        super().__init__(grps)
        self.master = master
        self.screen = pygame.display.get_surface()

        self.image = image
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.rect

        self.direction:pygame.Vector2 = direction
        self.speed = 4
        self.damage = 15

    def check_bounds_coll(self):

        for rect in self.master.level.bounds:
            if self.rect.colliderect(rect):
                self.kill()

    def check_player_hit(self):

        if not self.master.player.invincible and self.master.player.sprite_box.colliderect(self.rect):
            self.master.player.got_hit(self)
            self.kill()

    def move(self):

        self.pos += self.direction * self.speed * self.master.dt
        self.rect.center = self.pos

    def draw(self):
        
        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)

    def update(self):

        self.move()
        self.check_bounds_coll()
        self.check_player_hit()
