import sys, os
import pygame
import time


def load_image(name):
    fullname = os.path.join('data/', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()

def start_screen(screen, width, height, clock, fps):
    fon = pygame.transform.scale(load_image('fon/start_screen.png'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # 390 718
                # 300 589
                if 390 <= x <= 718 and 300 <= y <= 589:
                    st = settings(screen, width, height, clock, fps)
                    return st
                elif 819 <= x <= 1034 and 249 <= y <= 435:
                    leaders(screen, width, height, clock, fps)


        pygame.display.flip()
        clock.tick(fps)


def leaders(screen, width, height, clock, fps):
    file = open('data/lead/leads.txt', 'r', encoding='UTF8')
    lel = []
    for line in file:
        lel.append(line)
    file.close()
    fon = pygame.transform.scale(load_image('fon/leaders.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in lel:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 350
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                fon = pygame.transform.scale(load_image('fon/start_screen.png'), (width, height))
                screen.blit(fon, (0, 0))
                return
        pygame.display.flip()
        clock.tick(fps)
        # 819 1034
        #249 435

def settings(screen, width, height, clock, fps):
    fon = pygame.transform.scale(load_image('fon/settings.png'), (width, height))
    screen.blit(fon, (0, 0))
    text = 'this text is editable'
    font = pygame.font.SysFont(None, 48)
    img = font.render(text, True, (255, 0, 0))

    rect = img.get_rect()
    rect.topleft = (280, 82)
    cursor = pygame.Rect(rect.topright, (3, rect.height))



    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(text) > 0:
                        text = text[:-1]
                else:
                    text += event.unicode
                img = font.render(text, True, (0, 0, 0))
                rect.size = img.get_size()
                cursor.topleft = rect.topright
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 224 <= x <= 497 and 310 <= y <= 624:
                    return 1
                if 612 <= x <= 885 and 310 <= y <= 624:
                    return 0
            screen.blit(img, rect)
            if time.time() % 1 > 0.5:
                pygame.draw.rect(screen, (0, 0, 0), cursor)
        pygame.display.flip()
        clock.tick(fps)

