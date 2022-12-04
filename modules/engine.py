import pygame, os

class CustomGroup(pygame.sprite.Group):

    def draw(self):

        for sprite in self.sprites():
            sprite.draw()

class YSortGroup(pygame.sprite.Group):

    def draw_y_sort(self, key):

        for sprite in sorted((self.sprites()), key=key):
            sprite.draw()



def import_spritesheet(folder_path, sheet_name):
    "imports a given spritesheet and places it in a list"
    sprite_list = []
    name, size = sheet_name[:-4].split('-')
    w, h = [int(x) for x in size.split('x')]
    sheet = pygame.image.load(F"{folder_path}/{sheet_name}").convert_alpha()
    for i in range(sheet.get_width()//w):
        # sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        # sprite.blit(sheet, (-w*i, 0))
        sprite = sheet.subsurface((w*i, 0, w, h))
        sprite_list.append(sprite)
    return sprite_list


def import_sprite_sheets(folder_path):
    "imports all sprite sheets in a folder"
    animations = {}

    for file in os.listdir(folder_path):
        if file.endswith(".png"):
            animations[file.split('-')[0]] = import_spritesheet(folder_path, file)

    return animations

def load_pngs(folder_path):
    "loads all png from folder"

    return [pygame.image.load(F"{folder_path}/{file}").convert() for file in sorted(os.listdir(folder_path))]

def dist_sq(p1, p2):

    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2