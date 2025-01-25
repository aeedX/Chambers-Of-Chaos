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

def save():
    pass

def cut_sheet(sheet, rows, cols):
    rect = pygame.Rect(0, 0, sheet.get_width() // cols, sheet.get_height() // rows)
    frames = []
    for y in range(rows):
        for x in range(cols):
            frames.append(sheet.subsurface(pygame.Rect((rect.w * x, rect.h * y), rect.size)))
    return frames


class level:
    def __init__(self):
        self.bg = None
        self.lvl_obstacles = None
        self.load_level(0)


    def load_level(self, lvl_id):
        self.bg = load_image(f'sprites/levels/{lvl_id}_bg.png')
        self.lvl_obstacles = load_image(f'sprites/levels/{lvl_id}_obs.png')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.rect = pygame.Rect(0, 0, 75, 95)
        img_run = load_image('sprites/player/running.png')
        img_attack = load_image('sprites/player/attack.png')
        img_fall = load_image('sprites/player/fall.png')
        self.frames = [cut_sheet(self.rect, img_attack, 1, 10)[:1],
                       cut_sheet(self.rect, img_run, 1, 10),
                       cut_sheet(self.rect, img_attack, 1, 10),
                       cut_sheet(self.rect, img_fall, 1, 9)]
        self.frame = 0
        self.state = 0
        self.image = self.frames[self.state][self.frame]

    def action(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.state = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.state = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.frame = 0
            if event.button == 1:
                self.state = 2


    def update(self):
        if self.state == 2:
            self.frame = (self.frame + 1)
            if self.frame >= len(self.frames[self.state]):
                self.state = 0
                self.frame = 0
        elif self.state == 3:
            frame = (self.frame + 1)
            if frame < len(self.frames[self.state]):
                self.frame = frame
        else:
            self.frame = (self.frame + 1) % len(self.frames[self.state])
        self.image = self.frames[self.state][self.frame]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(enemies_group, all_sprites)
        self.running = []
        self.attack = []
        self.rect = pygame.Rect(0, 0, width, height)
