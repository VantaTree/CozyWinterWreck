import pygame
from .engine import *

attack_animations = {}

class PlayerAttack:

    def __init__(self, master):

        self.master = master
        self.player = self.master.player
        attack_animations.update(import_sprite_sheets("graphics/attacks"))

        self.slash_duration = 800

        self.SPAWN_SLASH_TIMER = pygame.event.custom_type()
        
        pygame.time.set_timer(self.SPAWN_SLASH_TIMER, self.slash_duration)

        self.EVENTS = (self.SPAWN_SLASH_TIMER)

    def process_events(self):

        for event in pygame.event.get(self.EVENTS):
            if event.type == self.SPAWN_SLASH_TIMER:
                SpriteAttack(self.master, [self.master.level.mask_attack_grp],
                "slash", (self.player.sprite_box.centerx + 10, self.player.sprite_box.centery - 20),
                15)

    def update(self):

        self.process_events()


class SpriteAttack(pygame.sprite.Sprite):

    def __init__(self, master, grps, anim, pos, power, duration=80, repeat=True, anim_speed=0.15) -> None:

        super().__init__(grps)
        self.master = master

        self.screen = pygame.display.get_surface()

        self.pos = pygame.Vector2(pos)
        self.animation = attack_animations[anim]
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=self.pos)

        self.anim_index = 0
        self.anim_speed = anim_speed

        self.power = power
        self.repeat = repeat
        
        self.duration = duration
        self.KILL_TIMER = pygame.event.custom_type()
        pygame.time.set_timer(self.KILL_TIMER, duration)

        self.EVENTS = (self.KILL_TIMER)

    def process_events(self):

        for event in pygame.event.get(self.EVENTS):
            if event.type == self.KILL_TIMER:
                self.kill()

    def check_enemy_hit(self):

        for enemy in self.master.level.enemy_grp.sprites():
            if not enemy.invincible and self.rect.colliderect(enemy.sprite_box):
                attack_mask = pygame.mask.from_surface(self.image)
                enemy_mask = pygame.mask.Mask(enemy.sprite_box.size, True)
                if attack_mask.overlap(enemy_mask, (enemy.sprite_box.x-self.rect.x, enemy.sprite_box.y-self.rect.y)):
                    enemy.got_hit(self.power, -enemy.direction)

    def update_image(self):

        try:
            self.image = self.animation[int(self.anim_index)]
        except IndexError:
            if self.repeat:
                self.image = self.animation[0]
                self.anim_index = 0
            else:
                self.kill()
                return

        self.anim_index += self.anim_speed * self.master.dt

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)

    def update(self):

        self.process_events()
        self.update_image()
        self.check_enemy_hit()


class Projectile(pygame.sprite.Sprite):

    def __init__(self, master, grps, anim, pos, direction, speed, damage, resistance = 1):

        super().__init__(grps)
        self.master = master
        self.screen = pygame.display.get_surface()

        self.animation = attack_animations[anim]
        self.image = self.animation[0]
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.rect

        self.anim_index = 0
        self.anim_speed = 0.1

        self.direction:pygame.Vector2 = direction
        self.speed = speed
        self.damage = damage
        self.resistance = resistance

    def check_bounds_coll(self):

        for rect in self.master.level.bounds:
            if rect.collidepoint(self.pos):
                self.kill()

    def check_hit(self): pass

    def check_player_hit(self):

        if not self.master.player.invincible and self.master.player.sprite_box.colliderect(self.rect):
            self.master.player.got_hit(self)
            self.kill()

    def check_enemy_hit(self):

        for enemy in self.master.level.enemy_grp.sprites():
            if not enemy.invincible and enemy.sprite_box.colliderect(self.rect):
                enemy.got_hit(self.damage, self.direction)
                self.resistance -= 1
                if self.resistance <= 0:
                    self.kill()

    def move(self):

        self.pos += self.direction * self.speed * self.master.dt
        self.rect.center = self.pos

    def update_image(self):
        
        try:
            self.image = self.animation[int(self.anim_index)]
        except IndexError:
            self.image = self.animation[0]
            self.anim_index = 0

        self.anim_index += self.anim_speed * self.master.dt

    def draw(self):
        
        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)

    def update(self):

        self.move()
        self.check_bounds_coll()
        self.update_image()
        self.check_hit()


# class PoisonAttack(pygame.sprite.Sprite):

#     def __init__(self, master, grps, anim, pos, damage, anim_speed=0.1):

#         super().__init__(grps)
#         self.master = master
#         self.screen = pygame.display.get_surface()

#         self.animation = attack_animations[anim]
#         self.image = self.animation[0]
#         self.pos = pygame.Vector2(pos)
#         self.rect = self.image.get_rect(center=self.pos)
#         self.hitbox = self.rect

#         self.frame_index = 0
#         self.anim_speed = anim_speed

#         self.damage = damage

#         pass