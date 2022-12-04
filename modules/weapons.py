import pygame
from .engine import *
from random import choice

attack_animations = {}

class PlayerAttack:

    def __init__(self, master):

        self.master = master
        self.player = self.master.player
        attack_animations.update(import_sprite_sheets("graphics/attacks"))
        attack_animations["slash_flipped"] = [pygame.transform.flip(img, True, True) for img in attack_animations["slash"]]

        self.slash_damage = [8, 8, 10, 10, 12, 12, 15, 15, 15]
        self.proj_damage = [0, 0, 0, 8, 8, 11, 11, 15, 15]
        self.proj_resistance = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        self.poison_damage = [0, 0, 0, 0, 0, 0, 3, 3, 6]

        self.slash_duration = 1_600
        self.proj_duration = 3_500
        self.poison_duration = 2_500

        self.SPAWN_SLASH_TIMER = pygame.event.custom_type()
        self.SPAWN_PROJ_TIMER = pygame.event.custom_type()
        self.SPAWN_POISON_TIMER = pygame.event.custom_type()
        
        pygame.time.set_timer(self.SPAWN_SLASH_TIMER, self.slash_duration)
        pygame.time.set_timer(self.SPAWN_PROJ_TIMER, self.proj_duration)
        pygame.time.set_timer(self.SPAWN_POISON_TIMER, self.poison_duration)

        self.EVENTS = (self.SPAWN_SLASH_TIMER, self.SPAWN_PROJ_TIMER, self.SPAWN_POISON_TIMER)

    def process_events(self):

        stage = self.master.enemy_handler.stage

        for event in pygame.event.get(self.EVENTS):
            if event.type == self.SPAWN_SLASH_TIMER:
                damage = self.slash_damage[stage]
                SpriteAttack(self.master, [self.master.level.mask_attack_grp], "slash", (10, -20), damage, repeat=False, anim_speed=0.52)
                if stage >= 1:
                    SpriteAttack(self.master, [self.master.level.mask_attack_grp], "slash_flipped", (-10, 20), damage, repeat=False, anim_speed=0.52)
                    self.master.sound.dict["slash_attack_2"].play()
                else: self.master.sound.dict["slash_attack_2"].play()

            if event.type == self.SPAWN_PROJ_TIMER:
                if stage < 3: continue

                enemy_sprites = list(self.master.level.enemy_grp.sprites())
                if not enemy_sprites: continue

                damage = self.proj_damage[stage]
                res = self.proj_resistance[stage]
                amount = stage - 2
                if amount <= 0: amount = 1
                elif amount > 3: amount = 3

                for _ in range(amount):
                    direction = - choice(enemy_sprites).direction
                    proj = Projectile(self.master, [self.master.level.y_sort_grp, self.master.level.enemy_projectile_grp],
                    'projectile_black', self.master.player.sprite_box.center, direction, 3, damage, res)
                    proj.check_hit = proj.check_enemy_hit
                self.master.sound.dict["fireball"].play()

            if event.type == self.SPAWN_POISON_TIMER:
                if stage < 6: continue

                damage = self.poison_damage[stage]
                if stage == 6:
                    SpriteAttack(self.master, [self.master.level.mask_attack_grp], "poison_med", (0, 0), damage, repeat=False, anim_speed = 0.08)
                elif stage >= 7:
                    SpriteAttack(self.master, [self.master.level.mask_attack_grp], "poison_big", (0, 0), damage, repeat=False, anim_speed = 0.08)
                self.master.sound.dict["poison_attack"].play()
                
    def update(self):

        self.process_events()


class SpriteAttack(pygame.sprite.Sprite):

    def __init__(self, master, grps, anim, offset, power, duration=80, repeat=True, anim_speed=0.15) -> None:

        super().__init__(grps)
        self.master = master

        self.screen = pygame.display.get_surface()

        self.pos = pygame.Vector2(offset) + self.master.player.sprite_box.center
        self.type = anim
        self.animation = attack_animations[anim]
        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=self.pos)

        self.anim_index = 0
        self.anim_speed = anim_speed

        self.power = power
        self.repeat = repeat
        
        self.duration = duration
        self.KILL_TIMER = CustomTimer()
        if repeat:
            self.KILL_TIMER.start(duration)

        # self.EVENTS = (self.KILL_TIMER)

    def process_events(self):

        # for event in pygame.event.get(self.EVENTS):
        if self.KILL_TIMER.check():
            self.kill()

    def check_enemy_hit(self):

        for enemy in self.master.level.enemy_grp.sprites():
            if not enemy.invincible and self.rect.colliderect(enemy.sprite_box):
                attack_mask = pygame.mask.from_surface(self.image)
                enemy_mask = pygame.mask.Mask(enemy.sprite_box.size, True)
                if attack_mask.overlap(enemy_mask, (enemy.sprite_box.x-self.rect.x, enemy.sprite_box.y-self.rect.y)):
                    if 'poison' in self.type:
                        enemy.got_hit(self.power, pygame.Vector2(0, 0))
                    else:
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

        if not self.master.player.invincible and self.master.player.sprite_box.collidepoint(self.pos):
            self.master.player.got_hit(self)
            self.master.sound.dict["fireball_hit"].play()
            self.kill()

    def check_enemy_hit(self):

        for enemy in self.master.level.enemy_grp.sprites():
            if not enemy.invincible and enemy.sprite_box.collidepoint(self.pos):
                enemy.got_hit(self.damage, self.direction)
                # self.master.sound.dict["fireball_hit"].play()
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