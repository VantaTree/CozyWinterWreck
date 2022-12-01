import pygame
from .world import World

class Game:

    def __init__(self, master) -> None:
        
        self.master = master
        master.game = self

        self.screen = pygame.display.get_surface()
        self.world = World(master)
    
    def draw(self):

        self.world.draw_background()
        self.world.draw_foreground()
        self.world.draw_debug()

    def process_events(self):
        pass

    def update(self):
        pass

    def run(self):
        
        self.process_events()
        self.update()
        self.draw()