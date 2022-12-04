import pygame

class PlayerUI:

    def __init__(self, master):

        self.master = master
        master.ui = self
        self.screen = pygame.display.get_surface()

        self.ui_bg = pygame.image.load("graphics/ui/player_ui.png").convert_alpha()
        self.abilities_ui = pygame.image.load("graphics/ui/abilities.png").convert_alpha()

        self.health_color = (214, 32, 17)
        self.xp_color = (142, 33, 106)

        self.ui_bar_width = 201

    def draw(self):
        stage = self.master.enemy_handler.stage
        if stage <= 2:
            show_length = 42
        elif stage <= 5:
            show_length = 42*2
        else:
            show_length = 42*3

        self.screen.blit(self.ui_bg, (10, 10))
        self.screen.blit(self.abilities_ui, (10, 10), (0, 0, show_length, 80))

        health_width = self.ui_bar_width * (self.master.player.health/self.master.player.max_health)
        if health_width < 0: health_width = 0

        pygame.draw.rect(self.screen, self.health_color, (34, 16, int(health_width), 4))
        try:
            xp_width = self.ui_bar_width * (self.master.enemy_handler.enemies_killed/self.master.enemy_handler.enemies_required[stage])
            pygame.draw.rect(self.screen, self.xp_color, (34, 31, int(xp_width), 4))
        except IndexError:pass