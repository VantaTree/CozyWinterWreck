import pygame
from .world import World
from .menus import PauseMenu

class Game:

    def __init__(self, master) -> None:
        
        self.master = master
        master.game = self

        self.screen = pygame.display.get_surface()
        self.world = World(master)
        self.pause_menu = PauseMenu(master)

        self.paused = False

    def pause_game(self):

        if not self.paused:
            self.paused = True
            self.pause_menu.open()

    
    def draw(self):

        self.world.draw_background()


        self.world.draw_foreground()
        self.world.draw_debug()

    def process_events(self):
        pass

    def run_pause_menu(self):
        self.pause_menu.update()
        self.pause_menu.draw()

    def update(self):

        self.world.update()

    def run(self):

        # self.master.music.can_play = not self.paused
        
        if self.paused:
            self.run_pause_menu()
        else:
            self.process_events()
            self.update()
            self.draw()