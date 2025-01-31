import pygame
import sys, os

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

tile_width = tile_height = 64

def load_image(name):
    fullname = os.path.join('data/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image

tile_images = {
    'wall': load_image('sprites/tiles/wall.png'),
    'floor': load_image('sprites/tiles/floor.png'),
    'lava': load_image('sprites/tiles/lava.png'),
    'chest': load_image('sprites/tiles/chest.png'),
    'exit': load_image('sprites/tiles/floor.png')
}

def save():
    pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Level:
    def __init__(self):
        self.lvl_id = 0
        self.lvl = []
        self.spawnpoints = []
        self.load_level(self.lvl_id)

    def load_level(self, lvl_id):
        lvl_map = map(str.strip, open(f'data/levels/{lvl_id}.txt', 'r'))
        lvl = [[s for s in row] for row in lvl_map]

        tiles_group.empty()
        for y in range(len(lvl)):
            for x in range(len(lvl[y])):
                if lvl[y][x] == '.':
                    Tile('floor', x, y)
                elif lvl[y][x] == '#':
                    Tile('wall', x, y)
                elif lvl[y][x] == '@':
                    # герой
                    Tile('floor', x, y)
                    self.spawnpoints.append(('player', x * tile_width + tile_width / 2, (y + 1) * tile_height))
                elif lvl[y][x] == '*':
                    Tile('lava', x, y)
                elif lvl[y][x] == '%':
                    # слайм
                    Tile('floor', x, y)
                    self.spawnpoints.append(('slime', x * tile_width + tile_width / 2, (y + 1) * tile_height))
                elif lvl[y][x] == '&':
                    # сундук
                    Tile('floor', x, y)
                    Tile('chest', x, y)
                elif lvl[y][x] == '$':
                    # скелет
                    Tile('floor', x, y)
                    self.spawnpoints.append(('skeleton', x * tile_width + tile_width / 2, (y + 1) * tile_height))
                elif lvl[y][x] == '?':
                    # дракон
                    Tile('floor', x, y)
                    self.spawnpoints.append(('dragon', x * tile_width + tile_width / 2, (y + 1) * tile_height))
                elif lvl[y][x] == '^':
                    # босс
                    Tile('floor', x, y)
                    self.spawnpoints.append(('ork', x * tile_width + tile_width / 2, (y + 1) * tile_height))
                elif lvl[y][x] == '!':
                    # выход
                    Tile('floor', x, y)
                    Tile('exit', x, y)


def cut_sheet(sheet, rows, cols):
    rect = pygame.Rect(0, 0, sheet.get_width() // cols, sheet.get_height() // rows)
    frames = []
    for y in range(rows):
        for x in range(cols):
            frames.append(sheet.subsurface(pygame.Rect((rect.w * x, rect.h * y), rect.size)))
    return frames


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.x, self.y = 100, 100
        self.direction, self.attack = 0, 0
        self.rect = pygame.Rect(0, 0, 0, 0)
        img_run = load_image('sprites/player/running.png')
        img_attack = load_image('sprites/player/attack.png')
        self.frames = [cut_sheet(img_attack, 1, 10)[:1],
                       cut_sheet(img_run, 1, 10),
                       cut_sheet(img_attack, 1, 10)]
        self.frame, self.state = 0, 0
        self.flip = False
        self.image = self.frames[self.state][self.frame]

    def action(self, event):
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_w:
                self.direction = 1
            elif event.key == pygame.K_a:
                self.direction = 2
            elif event.key == pygame.K_s:
                self.direction = 3
            elif event.key == pygame.K_d:
                self.direction = 4
        elif event.type == pygame.KEYUP:
            if self.direction == 1 and event.key == pygame.K_w or\
                    self.direction == 2 and event.key == pygame.K_a or\
                    self.direction == 3 and event.key == pygame.K_s or\
                    self.direction == 4 and event.key == pygame.K_d:
                self.direction = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.state != 2:
                    self.frame, self.state = 0, 2

        if self.direction and not self.state == 2:
            self.state = 1
        elif not self.state == 2:
            self.frame, self.state = 0, 0

    def update(self):
        if self.state == 1:
            self.frame = (self.frame + 1) % len(self.frames[self.state])
        elif self.state == 2:
            self.frame = (self.frame + 1)
            if self.frame >= len(self.frames[self.state]):
                self.frame, self.state = 0, 0
                self.attack = 0
        self.image = pygame.transform.flip(self.frames[self.state][self.frame], self.flip, False)
        w, h = self.image.get_width(), self.image.get_height()
        x, y = round(self.x - w / 2), round(self.y - h)
        self.rect = pygame.Rect(x, y, w, h)

        if self.direction == 1:
            self.y -= 5
        elif self.direction == 2:
            self.flip = False
            self.x -= 5
        elif self.direction == 3:
            self.y += 5
        elif self.direction == 4:
            self.flip = True
            self.x += 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(enemies_group, all_sprites)
        self.running = []
        self.attack = []
        self.rect = pygame.Rect(0, 0, width, height)
