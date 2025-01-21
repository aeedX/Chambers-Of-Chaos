import pygame
import sys, os

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def load_level():
    pass

def save():
    pass

def cut_sheet(rect, sheet, col_from, row_from, col_to, row_to):
    frames = []
    for y in range(row_from, row_to):
        for x in range(col_from, col_to):
            frames.append(sheet.subsurface(pygame.Rect((rect.w * x, rect.h * y), rect.size)))
    return frames


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.rect = pygame.Rect(0, 0, 98, 100)
        self.running = cut_sheet(self.rect, load_image('sprites/'))
        self.attack = []


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(enemies_group, all_sprites)
        self.running = []
        self.attack = []
        self.rect = pygame.Rect(0, 0, width, height)
