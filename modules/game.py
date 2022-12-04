import pygame
from .world import World
from .menus import PauseMenu
from .cutscene import StageCutScene

class Game:

    def __init__(self, master) -> None:
        
        self.master = master
        master.game = self

        self.screen = pygame.display.get_surface()
        self.world = World(master)
        self.pause_menu = PauseMenu(master)
        self.stage_scene = StageCutScene(master)

        self.paused = False
        self.stage_change = False

    def progress_stage(self):

        self.stage_change = True
        self.stage_scene.start()


    def pause_game(self):

        if not self.paused:
            self.paused = True
            self.pause_menu.open()

    
    def draw(self):

        self.world.draw_background()


        self.world.draw_foreground()
        # self.world.draw_debug()

    def process_events(self):
        pass

    def reset_game(self):

        p = self.master.player
        p.health = p.max_health
        p.hitbox.midbottom = p.start_pos
        p.dead = False

        h = self.master.enemy_handler
        h.stage = 0
        h.enemies_killed = 0

        self.master.level.enemy_grp.empty()
        self.master.level.y_sort_grp.empty()
        self.master.level.enemy_projectile_grp.empty()

        self.master.app.state = self.master.app.MAIN_MENU

        self.master.level.y_sort_grp.add(p)

    def run_pause_menu(self):
        self.pause_menu.update()
        self.pause_menu.draw()

    def update(self):

        self.world.update()

    def run(self):

        if self.master.player.dead:
            
            self.screen.fill((0,0,0))
            text1 = self.master.font_big.render("YOU DIED!!", True, "white")
            text2 = self.master.font_big.render("Press Enter to Restart", True, "white")

            self.screen.blit(text1, (215, 200))
            self.screen.blit(text2, (215, 300))

            for event in pygame.event.get(pygame.KEYDOWN):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reset_game()


        elif self.stage_change:
            
            self.stage_change = self.stage_scene.run()

        elif self.paused:
            self.run_pause_menu()
        else:
            self.process_events()
            self.update()
            self.draw()
