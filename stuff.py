import pygame
import sys, os

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

def load_image(name):
    fullname = os.path.join('data/', name)
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

def cut_sheet(rect, sheet, rows, cols):
    rect = pygame.Rect(0, 0, sheet.get_width() // cols, sheet.get_height() // rows)
    frames = []
    for y in range(rows):
        for x in range(cols):
            frames.append(sheet.subsurface(pygame.Rect((rect.w * x, rect.h * y), rect.size)))
    return frames


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.rect = pygame.Rect(0, 0, 75, 95)
        self.frames = [cut_sheet(self.rect, load_image('sprites/player/running.png'), 1, 10),
                       cut_sheet(self.rect, load_image('sprites/player/attack.png'), 1, 10),
                       cut_sheet(self.rect, load_image('sprites/player/attack2.png'), 1, 10),
                       cut_sheet(self.rect, load_image('sprites/player/fall.png'), 1, 9)]
        self.frame = 0
        self.state = 1
        self.image = self.frames[self.state][self.frame]


    def update(self):
        self.image = self.frames[self.state][self.frame]
        self.frame = (self.frame + 1) % len(self.frames[self.state])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(enemies_group, all_sprites)
        self.running = []
        self.attack = []
        self.rect = pygame.Rect(0, 0, width, height)
