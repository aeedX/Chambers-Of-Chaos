import os
import sys

import pygame
import pygame.sprite



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level):
    p_coord, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                # герой
                Tile('empty', x, y)
            elif level[y][x] == '*':
                Tile('lava', x, y)
            elif level[y][x] == '%':
                # слайм
                Tile('empty', x, y)
            elif level[y][x] == '&':
                # сундук
                Tile('empty', x, y)
            elif level[y][x] == '$':
                # скелет
                Tile('empty', x, y)
            elif level[y][x] == '?':
                # дракон
                Tile('empty', x, y)
            elif level[y][x] == '^':
                # босс
                Tile('empty', x, y)
            elif level[y][x] == '!':
                # выход
                Tile('empty', x, y)

    # вернем игрока, а также размер поля в клетках
    return p_coord, x, y


tile_images = {
    'wall': load_image('sprites\levels\scene\wrick.png'),
    'empty': load_image('sprites\levels\scene\loor.png'),
    'lava': load_image('sprites/levels/scene/lava.png')
}

tile_width = tile_height = 100


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

"""if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 1700, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    FPS = 50
    step = 20
    start_screen()
    p_coord, level_x, level_y = generate_level(load_level('sprites/levels/scene/level4.txt'))
    all_sprites.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)"""
