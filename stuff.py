import pygame
import sys, os

gl_event = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

collision_group = pygame.sprite.Group()
damage_group = pygame.sprite.Group()

collision_tiles = ['wall']
damage_tiles = ['lava']
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
        tile_groups = [tiles_group, all_sprites]
        if tile_type in collision_tiles:
            tile_groups.append(collision_group)
        if tile_type in damage_tiles:
            tile_groups.append(damage_group)
        super().__init__(*tile_groups)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Level:
    def __init__(self):
        self.lvl_id = 1
        self.lvl = []
        self.spawnpoints = []
        self.load_level(self.lvl_id)

    def load_level(self, lvl_id):
        lvl_map = map(str.strip, open(f'data/levels/{lvl_id}.txt', 'r'))
        lvl = [[s for s in row] for row in lvl_map]

        tiles_group.empty()
        enemies_group.empty()
        for y in range(len(lvl)):
            for x in range(len(lvl[y])):
                if lvl[y][x] == '.':
                    Tile('floor', x, y)
                elif lvl[y][x] == '#':
                    Tile('wall', x, y)
                elif lvl[y][x] == '@':
                    # герой
                    Tile('floor', x, y)
                    for player in player_group:
                        player.x, player.y = x * tile_width + tile_width / 2, (y + 1) * tile_height
                elif lvl[y][x] == '*':
                    Tile('lava', x, y)
                elif lvl[y][x] == '%':
                    # слайм
                    Tile('floor', x, y)
                    Enemy('slime', x * tile_width + tile_width / 2, (y + 1) * tile_height)
                elif lvl[y][x] == '&':
                    # сундук
                    Tile('floor', x, y)
                    Tile('chest', x, y)
                elif lvl[y][x] == '$':
                    # скелет
                    Tile('floor', x, y)
                    Enemy('skeleton', x * tile_width + tile_width / 2, (y + 1) * tile_height)
                elif lvl[y][x] == '?':
                    # дракон
                    Tile('floor', x, y)
                    Enemy('dragon', x * tile_width + tile_width / 2, (y + 1) * tile_height)
                elif lvl[y][x] == '^':
                    # босс
                    Tile('floor', x, y)
                    Enemy('ork', x * tile_width + tile_width / 2, (y + 1) * tile_height)
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
        self.x, self.y = 200, 200
        self.px, self.py = self.x, self.y
        self.direction, self.attack = 0, 0
        self.rect = pygame.Rect(0, 0, 1, 1)
        knight_run = load_image('sprites/player/knight_running.png')
        knight_attack = load_image('sprites/player/knight_attack.png')
        archer_run = load_image('sprites/player/archer_running.png')
        archer_attack = load_image('sprites/player/archer_attack.png')
        self.frames = [[cut_sheet(knight_attack, 1, 10)[:1],
                       cut_sheet(knight_run, 1, 10),
                       cut_sheet(knight_attack, 1, 10)],
                       [cut_sheet(archer_attack, 1, 8)[:1],
                       cut_sheet(archer_run, 1, 8),
                       cut_sheet(archer_attack, 1, 8)]]
        self.frame, self.state, self.hero = 0, 0, 0
        self.flip = False
        self.image = self.frames[self.hero][self.state][self.frame]
        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 100

    def get_damage(self, damage):
        if gl_event.type == pygame.USEREVENT + 2:
            self.hp -= damage
            print(self.hp)

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

    def update_sprite(self):
        if self.state == 1:
            self.frame = (self.frame + 1) % len(self.frames[self.hero][self.state])
        elif self.state == 2:
            self.frame = (self.frame + 1)
            if self.frame >= len(self.frames[self.hero][self.state]):
                self.frame, self.state = 0, 0
                self.attack = 0
        self.image = pygame.transform.flip(self.frames[self.hero][self.state][self.frame], self.flip, False)
        w, h = self.image.get_width(), self.image.get_height()
        #w, h = 96, 96
        x, y = round(self.x - w / 2), round(self.y - h)
        self.rect = pygame.Rect(x, y, w, h)

    def update(self):
        if self.state == 2:
            return
        if self.direction:
            self.px, self.py = self.x, self.y
        if self.direction == 1:
            if self.hero:
                self.y += 2
            self.y -= 4
            self.py += 5
        elif self.direction == 2:
            self.flip = False
            if self.hero:
                self.flip = True
                self.x += 2
            self.x -= 4
            self.px += 5
        elif self.direction == 3:
            if self.hero:
                self.y -= 2
            self.y += 4
            self.py -= 5
        elif self.direction == 4:
            self.flip = True
            if self.hero:
                self.flip = False
                self.x -= 2
            self.x += 4
            self.px -= 5
        for sprite in collision_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.x, self.y = self.px, self.py
        for sprite in damage_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.get_damage(1)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, ceil_x, ceil_y):
        super().__init__(enemies_group, all_sprites)
        self.direction = 0
        self.rect = pygame.Rect(0, 0, 1, 1)
        running = load_image(f'sprites/enemies/{enemy_type}_running.png')
        attack = load_image(f'sprites/enemies/{enemy_type}_attack.png')
        if enemy_type == 'slime':
            self.frames = [cut_sheet(attack, 1, 6)[:1],
                           cut_sheet(running, 1, 6),
                           cut_sheet(attack, 1, 6)]
        elif enemy_type == 'skeleton':
            self.frames = [cut_sheet(attack, 1, 8)[:1],
                           cut_sheet(running, 1, 8),
                           cut_sheet(attack, 1, 8)]
        elif enemy_type == 'ork':
            self.frames = [cut_sheet(attack, 1, 4)[:1],
                           cut_sheet(running, 1, 7),
                           cut_sheet(attack, 1, 4)]
        else:
            self.frames = [cut_sheet(attack, 1, 2)[:1],
                           cut_sheet(running, 1, 4),
                           cut_sheet(attack, 1, 2)]
        self.frame, self.state = 0, 1
        self.flip = False
        self.image = self.frames[self.state][self.frame]
        self.x, self.y = round(ceil_x + tile_width / 2), ceil_y + tile_height
        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 100

    def get_damage(self, damage):
        if gl_event.type == pygame.USEREVENT + 2:
            self.hp -= damage
            print(self.hp)

    def action(self, event):
        if self.direction and not self.state == 2:
            self.state = 1
        elif not self.state == 2:
            self.frame, self.state = 0, 0

    def update_sprite(self):
        if self.state == 1:
            self.frame = (self.frame + 1) % len(self.frames[self.state])
        elif self.state == 2:
            self.frame = (self.frame + 1)
            if self.frame >= len(self.frames[self.state]):
                self.frame, self.state = 0, 0
                self.attack = 0
        self.image = pygame.transform.flip(self.frames[self.state][self.frame], self.flip, False)
        w, h = self.image.get_width(), self.image.get_height()
        # w, h = 96, 96
        x, y = round(self.x - w / 2), round(self.y - h)
        self.rect = pygame.Rect(x, y, w, h)

    def update(self):
        if self.state == 2:
            return
        if self.direction:
            self.px, self.py = self.x, self.y
        if self.direction == 1:
            self.y -= 4
            self.py += 5
        elif self.direction == 2:
            self.flip = False
            self.x -= 4
            self.px += 5
        elif self.direction == 3:
            self.y += 4
            self.py -= 5
        elif self.direction == 4:
            self.flip = True
            self.x += 4
            self.px -= 5
        for sprite in collision_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.x, self.y = self.px, self.py
        for sprite in damage_group:
            if pygame.sprite.collide_mask(self, sprite):
                self.get_damage(1)


def update_sprites():
    for sprite in enemies_group:
        sprite.update_sprite()
    for sprite in player_group:
        sprite.update_sprite()
