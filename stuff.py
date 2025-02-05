import pygame
import sys, os
from random import choice, randint
import json

from pygame.cursors import arrow

gl_event = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
horizontal_up_borders = pygame.sprite.Group()
vertical_left_borders = pygame.sprite.Group()
horizontal_down_borders = pygame.sprite.Group()
vertical_right_borders = pygame.sprite.Group()
borders_group = [horizontal_up_borders, horizontal_down_borders, vertical_right_borders, vertical_left_borders]
arrow_group = pygame.sprite.Group()
level_group = []

collision_group = pygame.sprite.Group()
damage_group = pygame.sprite.Group()
chest_group = pygame.sprite.Group()

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


def save(save_name, username, player, level):
    with open('data/saves/saves_data.json') as f:
        saves = json.load(f)
    f.close()
    if level == 4:
        os.remove(f'data/saves/{save_name}.json')
        del saves[saves.index(save_name)]
    else:
        with open(f'data/saves/{save_name}.json', 'w') as f:
            data = {
                'score': player.score,
                'hero': player.hero,
                'max_hp': player.max_hp,
                'damage': player.damage,
                'speed': player.speed,
                'lvl_id': level.lvl_id,
                'username': username
            }
            json.dump(data, f)
        f.close()
        if save_name not in saves:
            saves.append(save_name)
    with open('data/saves/saves_data.json', 'w') as f:
        json.dump(saves, f)
    f.close()

    with open('data/leaderboard.json', 'r') as f:
        table = json.load(f)
        print(table)
    f.close()
    with open('data/leaderboard.json', 'w') as f:
        if username in table.keys():
            if player.hero:
                if table[username] < player.score / 500:
                    table[username] = player.score / 500
            else:
                if table[username] < player.score / 1000:
                    table[username] = player.score / 1000
        else:
            if player.hero:
                table[username] = player.score / 500
            else:
                table[username] = player.score / 1000
        table = dict(reversed(sorted(table.items(), key=lambda item: item[1])))
        print(table)
        json.dump(table, f)
    f.close()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2 and x1 <= (tile_width * 2):  # вертикальная левая стенка
            self.add(vertical_left_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif x1 == x2 and x1 > (tile_width * 2):  # вертикальная правая стенка
            self.add(vertical_right_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif y1 == y2 and y1 <= (tile_height * 2):  # горизонтальная  верхняя стенка
            self.add(horizontal_up_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        else: # горизонтальная нижняя стенка
            self.add(horizontal_down_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        tile_groups = [tiles_group, all_sprites]
        if tile_type in collision_tiles:
            pass
            #tile_groups.append(collision_group)
        if tile_type in damage_tiles:
            tile_groups.append(damage_group)
        if tile_type == 'chest':
            tile_groups.append(chest_group)
            self.content = choice(('speed', 'hp', 'damage'))
        super().__init__(*tile_groups)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, x2, y2, damage=10):
        super().__init__(arrow_group)
        self.radius = radius
        self.tier = 3 # уровень пули
        self.dc = 0 # счетчик отскоков до смерти
        self.move_counter = 0
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        '''am_x = 1
        am_y = 1
        v_x = x2 - x
        v_y = y2 - y
        while v_x > 5:
            v_x = v_x / 5
            am_x += 1
        while v_y > 5:
            v_y = v_y / 5
            am_y += 1'''
        self.vx = (x2 - x) / 15 # скорость пули
        self.vy = (y2 - y) / 15 # скорость пули

        self.damage = damage

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        self.move_counter += 1
        if self.tier == 3:
            if pygame.sprite.spritecollideany(self, horizontal_up_borders) or\
                    pygame.sprite.spritecollideany(self, horizontal_down_borders):
                self.vy = -self.vy
                self.dc += 1
            if pygame.sprite.spritecollideany(self, vertical_left_borders) or \
                    pygame.sprite.spritecollideany(self, vertical_right_borders):
                self.vx = -self.vx
                self.dc += 1
            if self.move_counter == 150:
                self.kill()
        elif self.tier == 2:
            if self.move_counter == 15:
                self.kill()
            if pygame.sprite.spritecollideany(self, horizontal_up_borders) or\
                    pygame.sprite.spritecollideany(self, horizontal_down_borders) or\
                    pygame.sprite.spritecollideany(self, vertical_left_borders) or\
                    pygame.sprite.spritecollideany(self, vertical_right_borders):
                self.kill()
        else:
            if pygame.sprite.spritecollideany(self, enemies_group) or \
                    pygame.sprite.spritecollideany(self, horizontal_up_borders) or\
                    pygame.sprite.spritecollideany(self, horizontal_down_borders) or\
                    pygame.sprite.spritecollideany(self, vertical_left_borders) or\
                    pygame.sprite.spritecollideany(self, vertical_right_borders):
                self.kill()


class Level:
    def __init__(self, lvl_id):
        level_group.append(self)
        self.lvl_id = lvl_id
        self.lvl = []
        self.spawnpoints = []
        self.load_level()

    def load_level(self):
        lvl_map = map(str.strip, open(f'data/levels/{self.lvl_id}.txt', 'r'))
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
                        player.hp = player.max_hp
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
    def __init__(self, score, hero, max_hp, damage, speed):
        super().__init__(player_group, all_sprites)
        self.score = score
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
        self.frame, self.state, self.hero = 0, 0, hero
        self.flip = False
        self.image = self.frames[self.hero][self.state][self.frame]

        self.max_hp = max_hp
        self.hp = max_hp
        self.damage = damage
        self.speed = speed


    def get_damage(self, damage=0.5):
        #if gl_event.type == pygame.USEREVENT + 2:
        #    self.hp -= damage
        #    print(self.hp)

        self.hp -= damage
        print(self.hp)

        if self.hp <= 0:

            self.kill()

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
                if self.hero == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] >= self.x and self.flip == False:
                        Arrow(5, self.x, self.y - 50, pos[0], pos[1], damage=self.damage)
                    elif pos[0] <= self.x and self.flip == True:
                        Arrow(5, self.x - 10, self.y - 50, pos[0], pos[1], damage=self.damage)

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
        self.mask = pygame.mask.from_surface(self.image)
        w, h = self.image.get_width(), self.image.get_height()
        #w, h = 96, 96
        x, y = round(self.x - w / 2), round(self.y - h)
        self.rect = pygame.Rect(x, y, w, h)

    def update(self):
        go_flag = True
        tx = self.x
        ty = self.y
        px = self.x
        py = self.y
        for chest in chest_group:
            if pygame.sprite.collide_mask(self, chest) and self.state == 2:
                print(chest.content)
                if chest.content == 'speed':
                    self.speed += 1
                elif chest.content == 'hp':
                    self.max_hp += 50
                    self.hp += 50
                elif chest.content == 'damage':
                    self.damage += 5
                chest.kill()
        if self.state == 2:
            return
        if self.direction:
            px, py = tx, ty
        if self.direction == 1:
            ty -= self.speed
            py += self.speed
        elif self.direction == 2:
            self.flip = False
            if self.hero:
                self.flip = True
            tx -= self.speed
            px += self.speed

        elif self.direction == 3:
            ty += self.speed
            py -= self.speed
        elif self.direction == 4:
            self.flip = True
            if self.hero:
                self.flip = False
            tx += self.speed
            px -= self.speed

        if tx < 80 or tx > 1088 - 80 or ty < 160 or ty > 704 - 128:
            self.x, self.y = px, py
        else:
            self.x, self.y = tx, ty
        if pygame.sprite.spritecollideany(self, damage_group):
            for sprite in damage_group:
                if pygame.sprite.collide_mask(self, sprite):
                    self.get_damage(0.5)
        #self.x, self.y = tx, ty


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, x, y):
        super().__init__(enemies_group, all_sprites)
        self.direction = [0, 0]
        self.rect = pygame.Rect(0, 0, 1, 1)
        running = load_image(f'sprites/enemies/{enemy_type}_running.png')
        attack = load_image(f'sprites/enemies/{enemy_type}_attack.png')
        if enemy_type == 'slime':
            self.frames = [cut_sheet(attack, 1, 6)[:1],
                           cut_sheet(running, 1, 6),
                           cut_sheet(attack, 1, 6)]
            self.damage = 0.1
            self.speed = 2
        elif enemy_type == 'skeleton':
            self.frames = [cut_sheet(attack, 1, 8)[:1],
                           cut_sheet(running, 1, 8),
                           cut_sheet(attack, 1, 8)]
            self.damage = 1
            self.speed = 3
        elif enemy_type == 'ork':
            self.frames = [cut_sheet(attack, 1, 4)[:1],
                           cut_sheet(running, 1, 7),
                           cut_sheet(attack, 1, 4)]
            self.damage = 2
            self.speed = 3
        else:
            self.frames = [cut_sheet(attack, 1, 2)[:1],
                           cut_sheet(running, 1, 4),
                           cut_sheet(attack, 1, 2)]
            self.damage = 3
            self.speed = 2
        self.frame, self.state = 0, 1
        self.flip = False
        self.image = self.frames[self.state][self.frame]
        self.x, self.y = x, y
        self.mask = pygame.mask.from_surface(self.image)

        self.hp = 100

    def get_damage(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

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
        x, y = 0, 0
        for player in player_group:
            x, y = player.x, player.y
        tx, ty = self.x, self.y
        if x - self.x > abs(self.y - y):
            self.direction = 4
        elif self.x - x > abs(self.y - y):
            self.direction = 2
        elif y - self.y > abs(self.x - x):
            self.direction = 3
        else:
            self.direction = 1

        for arrow in arrow_group:
            if pygame.sprite.collide_mask(self, arrow):
                self.get_damage(arrow.damage)
                break
        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                if player.state == 2:
                    self.get_damage(player.damage)
                else:
                    player.get_damage(self.damage)
                break

        if self.state == 2:
            return
        if self.direction == 1:
            ty -= self.speed
            tx += randint(-self.speed, self.speed)
        elif self.direction == 2:
            self.flip = False
            tx -= self.speed
            tx += randint(-self.speed, self.speed)
        elif self.direction == 3:
            ty += self.speed
            ty += randint(-self.speed, self.speed)
        else:
            self.flip = True
            tx += self.speed
            ty += randint(-self.speed, self.speed)
        if not (tx < 80 or tx > 1088 - 80 or ty < 120 or ty > 704 - 128):
            self.x, self.y = tx, ty


def update_sprites():
    for sprite in enemies_group:
        sprite.update_sprite()
    for sprite in player_group:
        sprite.update_sprite()
