import pygame
from .frect import FRect
from .entity import Entity

class Player(Entity):

    def __init__(self, master):

        self.master = master
        master.player = self
        self.screen = pygame.display.get_surface()

        self.start_pos = 100, 100
        self.hitbox= FRect(*self.start_pos, 12, 9)

        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.hitbox.midbottom))

        self.direction = pygame.Vector2(1, 0)
        self.input_direc = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 0.8
        self.deceleration = 1.2
        self.max_speed = 3
        self.dash_speed = 12
        self.moving = False
        self.dashing = False
        self.can_dash = True

        self.DASH_FOR = pygame.event.custom_type()
        self.DASH_COOLDOWN_TIMER = pygame.event.custom_type()

        self.EVENTS = (pygame.KEYDOWN, self.DASH_FOR, self.DASH_COOLDOWN_TIMER
        )

    def update_image(self):

        self.rect.midbottom = self.hitbox.midbottom

    def get_input_and_events(self):
        
        keys = pygame.key.get_pressed()

        self.input_direc.update(0, 0)
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
                if event.key == pygame.K_SPACE and self.can_dash:
                    self.dashing = True
                    self.can_dash = False
                    pygame.time.set_timer(self.DASH_FOR, 100, loops = 1)
                    pygame.time.set_timer(self.DASH_COOLDOWN_TIMER, 650, loops=1)
                
            if event.type == self.DASH_FOR:
                self.dashing = False

            if event.type == self.DASH_COOLDOWN_TIMER:
                self.can_dash = True

    def move(self):

        if not self.dashing:
            if self.moving:
                self.velocity += self.direction * self.acceleration  * self.master.dt
            elif self.velocity.magnitude_squared() >= self.deceleration**2:
                self.velocity -= self.velocity.normalize() * self.deceleration  * self.master.dt
            else: self.velocity.update(0, 0)

            if (mag:=self.velocity.magnitude_squared()):
                if mag > self.max_speed**2:
                    self.velocity.scale_to_length(self.max_speed)
        else:
            self.velocity = self.direction * self.dash_speed

        self.hitbox.centerx += self.velocity.x * self.master.dt
        self.check_bounds_collision(0, self.master.level.bounds)
        self.hitbox.bottom += self.velocity.y * self.master.dt
        self.check_bounds_collision(1, self.master.level.bounds)

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)

    def update(self):

        self.get_input_and_events()
        self.move()
        self.update_image()
        self.master.debug("velocity: ", self.velocity)
        self.master.debug("dashing: ", self.dashing)
        self.master.debug("can_dash: ", self.can_dash)


