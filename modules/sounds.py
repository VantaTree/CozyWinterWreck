import os
import pygame

class SoundSet:

    def __init__(self, master):

        self.master = master
        self.master.sound = self
        self.dict = {}

        for sound_file in os.listdir("sounds"):
            if not sound_file.endswith(".ogg"): continue
            self.dict[sound_file[:-4]] = pygame.mixer.Sound(F"sounds/{sound_file}")
        
        self.dict["fireball_hit"].set_volume(0.4)
