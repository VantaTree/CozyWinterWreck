import pygame
from .config import *
from .engine import *


class StageCutScene:

    DORMANT = 0
    INC = 1
    HALT = 4
    OUT = 8

    def __init__(self, master):

        self.master = master
        self.screen = pygame.display.get_surface()
        self.bg_screen = None
        self.state = self.DORMANT
        self.close = False

        self.alpha_index = 0
        self.alpha_speed = 2

        self.card_surface = pygame.image.load("graphics/memory_stuff/dream_card.png").convert_alpha()
        self.card_rect = self.card_surface.get_rect(center = (W//2, H//2))
        self.no_time_surf = pygame.image.load("graphics/memory_stuff/no_time.png").convert_alpha()

        self.dream_button = pygame.image.load("graphics/memory_stuff/dream_button.png").convert_alpha()
        self.dream_button_rect = self.dream_button.get_rect(center = (W//2, H//2))

        

    def start(self):
        
        self.bg_screen = blur_image(pygame.display.get_surface())
        self.alpha_index = 0
        self.close = False
        self.state = self.INC
        self.master.sound.dict["Bad connection"].play()

    def draw(self):

        self.screen.blit(self.bg_screen, (0, 0))
        self.screen.blit(self.card_surface, self.card_rect)
        self.screen.blit(self.no_time_surf, self.card_rect)
        if self.state == self.HALT:
            self.screen.blit(self.dream_button, self.dream_button_rect)

    def update(self):

        if self.state == self.INC:
            self.alpha_index += self.alpha_speed * self.master.dt
            if self.alpha_index >= 255:
                self.alpha_index = 255
                self.state = self.HALT

        elif self.state == self.HALT:
            for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.card_rect.collidepoint(event.pos):
                        self.state = self.OUT
                        self.master.sound.dict["Good connection"].play()

        elif self.state == self.OUT:
            self.alpha_index -= self.alpha_speed * self.master.dt
            if self.alpha_index <= 0:
                self.state = self.DORMANT
                self.close = True

        if self.state in (self.INC, self.OUT):
            self.card_surface.set_alpha(int(self.alpha_index))
            self.no_time_surf.set_alpha(int(self.alpha_index))

    def run(self):

        self.update()
        self.draw()
        return not self.close