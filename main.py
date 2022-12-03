import pygame
from modules import *
from enum import Enum

class Master:
    
    def __init__(self) -> None:

        self.dt:float = 0
        self.app:App
        self.game:Game
        # self.world:World
        # self.debug:Debug
        # self.player:Player
        # self.level:Level

class State(Enum):

    MAIN_MENU = 1
    IN_GAME = 2


class App:

    def __init__(self) -> None:
        
        #window
        self.screen = pygame.display.set_mode((W, H), pygame.SCALED)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Winter Wreck Game")
        # pygame.display.set_icon()

        #init
        self.master = Master()
        self.master.app = self

        SoundSet(self.master)

        self.game = Game(self.master)

        self.state = State.IN_GAME

    def process_events(self):

        for event in pygame.event.get((pygame.QUIT, pygame.KEYUP)):
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit

    def run_app(self):

        if self.state == State.MAIN_MENU:
            pass
        elif self.state == State.IN_GAME:
            self.game.run()


    def run(self):

        while True:
            
            pygame.display.update()
            self.master.dt = self.clock.tick(FPS) / 16.667
            if self.master.dt > 12: self.master.dt = 12
            self.master.debug("FPS: ", round(self.clock.get_fps(), 2))
            self.process_events()
            self.run_app()
            pygame.event.pump()


if __name__ == "__main__":

    pygame.init()
    app = App()
    app.run()


