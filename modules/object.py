import pygame
from .config import *
from random import choice
import os

object_hitboxes = {
    "cabin": pygame.Rect(0, 0, 42,34),
    "rock":  pygame.Rect(0, 0, 12,6),
    "tree":  pygame.Rect(0, 0, 30,9),
    "gravestone": pygame.Rect(0, 0, 12, 2)
}

class Object(pygame.sprite.Sprite):

    def __init__(self, master, grps, type, pos):

        super().__init__(grps)
        self.master = master
        self.screen = pygame.display.get_surface()

        path = "graphics/map/objects/" + type + '/' + choice(os.listdir(F"graphics/map/objects/{type}"))

        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0]*TILESIZE, pos[1]*TILESIZE))
        self.hitbox = self.rect

        rect = object_hitboxes.get(type)
        if rect:
            bound = rect.copy()
            bound.midbottom = self.rect.midbottom
            self.master.level.bounds.append(bound)
        
        if type == 'cabin':
            Object(master, grps, 'torch', (pos[0]-1, pos[1]+4))
            Object(master, grps, 'torch', (pos[0]+3, pos[1]+4))


    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.world.offset)


# class AnimatedObject(Object):

#     def __init__(self, master, grps, type, image, pos):

#         super().__init__(master, grps, type, image, pos)

#         self.anim_index = 0
