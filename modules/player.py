import pygame
from .frect import FRect
from .entity import Entity
from math import sin
from .weapons import PlayerAttack

class Player(Entity):

    def __init__(self, master, grps):

        super().__init__(grps)
        self.master = master
        master.player = self
        self.screen = pygame.display.get_surface()

        self.start_pos = 672, 928
        self.hitbox= FRect(*self.start_pos, 12, 9)
        self.sprite_box = FRect(0, 0, 8, 30)

        self.original_image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(midbottom=(self.hitbox.midbottom))

        self.direction = pygame.Vector2(1, 0)
        self.input_direc = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 0.6
        self.deceleration = 1.0
        self.max_speed = 2.2
        self.dash_speed = 12
        self.kb_speed = 4
        self.moving = False
        self.in_control = True
        self.invincible = False
        self.dashing = False
        self.can_dash = True
        self.hurting = False

        self.max_health = 100
        self.health = self.max_health

        self.hit_kb_direc = pygame.Vector2(0, 0)
        self.invincibility_alpha = 255

        self.enemies_killed = 0

        self.attack_handler = PlayerAttack(master)

        self.dead = False

        self.DASH_FOR = pygame.event.custom_type()
        self.DASH_COOLDOWN_TIMER = pygame.event.custom_type()
        self.HURT_INVIS_TIMER = pygame.event.custom_type()
        self.HURTING_TIMER = pygame.event.custom_type()
        self.HEAL_TIMER = pygame.event.custom_type()

        pygame.time.set_timer(self.HEAL_TIMER, 3_000)

        self.EVENTS = (pygame.KEYDOWN, self.DASH_FOR, self.DASH_COOLDOWN_TIMER, self.HURT_INVIS_TIMER,
        self.HURTING_TIMER, self.HEAL_TIMER
        )
    
    def got_hit(self, object):

        self.health -= object.damage
        if self.health <= 0:
            self.dead = True
            return

        self.hit_kb_direc = object.direction

        self.dashing = False
        self.in_control = False
        self.invincible = True
        self.hurting = True

        pygame.time.set_timer(self.HURT_INVIS_TIMER, 1_200, loops=1)
        pygame.time.set_timer(self.HURTING_TIMER, 120, loops=1)

        self.master.sound.dict['damage'].play()

    def update_image(self):

        flip = self.velocity.x < 0
        self.image = pygame.transform.flip(self.original_image, flip, False)

        if self.invincible:
            self.invincibility_alpha = abs(sin(pygame.time.get_ticks())) * 255
            self.image.set_alpha(self.invincibility_alpha)
        self.rect.midbottom = self.hitbox.midbottom

    def get_input_and_events(self):
        
        self.input_direc.update(0, 0)

        if  self.in_control:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                self.input_direc.y += 1
            if keys[pygame.K_w]:
                self.input_direc.y -= 1
            if keys[pygame.K_d]:
                self.input_direc.x += 1
            if keys[pygame.K_a]:
                self.input_direc.x -= 1
        
        if self.input_direc.x and self.input_direc.y:
            self.input_direc.normalize_ip()
        if self.input_direc.x or self.input_direc.y:
            self.moving = True
            if not self.dashing:
                self.direction.update(self.input_direc)
        else: self.moving = False


        for event in pygame.event.get(self.EVENTS):

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.in_control and self.can_dash:
                    self.dashing = True
                    self.can_dash = False
                    pygame.time.set_timer(self.DASH_FOR, 100, loops = 1)
                    pygame.time.set_timer(self.DASH_COOLDOWN_TIMER, 650, loops=1)
                    self.master.sound.dict['dash'].play()
                if event.key == pygame.K_ESCAPE:
                    self.master.game.pause_game()
                
            if event.type == self.DASH_FOR:
                self.dashing = False

            if event.type == self.DASH_COOLDOWN_TIMER:
                self.can_dash = True

            if event.type == self.HURTING_TIMER:
                self.in_control = True
                self.hurting = False

            if event.type == self.HURT_INVIS_TIMER:
                self.invincible = False
                self.image.set_alpha(255)

            if event.type == self.HEAL_TIMER and self.health < self.max_health:
                self.health += 1


    def move(self):

        if self.hurting:
            self.velocity.update(self.hit_kb_direc*self.kb_speed)
        elif self.dashing:
            self.velocity = self.direction * self.dash_speed
        else:
            if self.moving:
                self.velocity += self.direction * self.acceleration  * self.master.dt
            elif self.velocity.magnitude_squared() >= self.deceleration**2:
                self.velocity -= self.velocity.normalize() * self.deceleration  * self.master.dt
            else: self.velocity.update(0, 0)

            if (mag:=self.velocity.magnitude_squared()):
                if mag > self.max_speed**2:
                    self.velocity.scale_to_length(self.max_speed)
            

        self.hitbox.centerx += self.velocity.x * self.master.dt
        self.check_bounds_collision(0, self.master.level.bounds)
        self.hitbox.bottom += self.velocity.y * self.master.dt
        self.check_bounds_collision(1, self.master.level.bounds)

        self.sprite_box.midbottom = self.hitbox.midbottom

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)

    def update(self):

        self.get_input_and_events()
        self.move()
        self.update_image()
        self.attack_handler.update()
        # self.master.debug("pos: ", self.rect.center)
        # self.master.debug("velocity: ", self.velocity)
        # self.master.debug("dashing: ", self.dashing)
        # self.master.debug("can_dash: ", self.can_dash)
        # self.master.debug("health: ", self.health)


