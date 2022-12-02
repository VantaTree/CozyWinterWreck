import pygame
from .world import World
from .player import Player

class Game:

    def __init__(self, master) -> None:
        
        self.master = master
        master.game = self

        self.screen = pygame.display.get_surface()
        self.world = World(master)

        self.player = Player(master)
    
    def draw(self):

        self.world.draw_background()

        self.player.draw()

        self.world.draw_foreground()
        self.world.draw_debug()

    def process_events(self):
        pass

    def update(self):

        self.player.update()
        self.world.update()

    def run(self):
        
        self.process_events()
        self.update()
        self.draw()