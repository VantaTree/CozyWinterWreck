import pygame

class Entity:

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
        self.sprite_list = []

    def add(self, sprite):

        self.sprite_list.append(sprite)

    def draw(self):

        for sprite in self.sprite_list:
            sprite.draw()

    def draw_y_sort(self, key):

        for sprite in sorted(self.sprite_list, key=key):
            sprite.draw()

    def update(self, *args, **kwargs):

        for sprite in self.sprite_list:
            sprite.update(*args, **kwargs)
        
