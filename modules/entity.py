import pygame

class Entity(pygame.sprite.Sprite):

    def __init__(self, grps):
        super().__init__(grps)

    def check_bounds_collision(self, axis, bounds):

        if axis == 0: #x
            
             for rect in bounds:
                if self.hitbox.colliderect(rect):

                    if self.velocity.x > 0:
                        self.hitbox.right = rect.left
                        return 1
                    elif self.velocity.x < 0:
                        self.hitbox.left = rect.right
                        return -1

        if axis == 1: #y

            for rect in bounds:
                if self.hitbox.colliderect(rect):

                    if self.velocity.y > 0:
                        self.hitbox.bottom = rect.top
                        return 1
                    elif self.velocity.y < 0:
                        self.hitbox.top = rect.bottom
                        return -1

class SpriteGroup:

    def __init__(self, master, type):

        self.master = master
        self.screen = pygame.display.get_surface()
        self.type = type
        self.sprites = []

    def add(self, sprite):

        self.sprites.append(sprite)

    def draw(self):

        for sprite in self.sprites:
            sprite.draw()

    def draw_y_sort(self, key):

        for sprite in sorted(self.sprites, key=key):
            sprite.draw()

    def update(self, *args, **kwargs):

        for sprite in self.sprites:
            sprite.update(*args, **kwargs)
        

class YSortGroup(pygame.sprite.Group):

    def draw_y_sort(self, key):

        for sprite in sorted((self.sprites()), key=key):
            sprite.draw()
