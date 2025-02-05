import sys
import pygame
import stuff
import json


def terminate():
    sys.exit()

def start_screen(screen):
    selection = 0

    font = pygame.font.SysFont(None, 48)
    tip = font.render('arrows for navigation, space bar for selection', True, (33, 33, 33))
    new_game_btn = font.render('NEW GAME', True, (66, 66, 66))
    load_game_btn = font.render('LOAD GAME', True, (66, 66, 66))
    leaders_btn = font.render('LEADERS', True, (66, 66, 66))
    exit_btn = font.render('EXIT', True, (66, 66, 66))
    active_btns = [(font.render('NEW GAME', True, (123, 123, 123)), (20, 20)),
              (font.render('LOAD GAME', True, (123, 123, 123)), (20, 120)),
              (font.render('LEADERS', True, (123, 123, 123)), (20, 220)),
              (font.render('EXIT', True, (123, 123, 123)), (20, 320))]

    main_running = True
    while main_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and selection < 3:
                    selection += 1
                elif event.key == pygame.K_UP and selection > 0:
                    selection -= 1
                elif event.key == pygame.K_SPACE:
                    if selection == 0:
                        save = new_game(screen)
                        if save != None:
                            return stuff.Player(*save[:5]), stuff.Level(save[5]), *save[6:]
                    elif selection == 1:
                        save = load_game(screen)
                        if save != None:
                            return stuff.Player(*save[:5]), stuff.Level(save[5]), *save[6:]
                    elif selection == 2:
                        leaders(screen)
                    elif selection == 3:
                        terminate()
        screen.fill((0, 0, 0))
        screen.blit(new_game_btn, (20, 20))
        screen.blit(load_game_btn, (20, 120))
        screen.blit(leaders_btn, (20, 220))
        screen.blit(exit_btn, (20, 320))
        screen.blit(*active_btns[selection])
        screen.blit(tip, (20, 650))

        pygame.display.flip()


def new_game(screen):
    selection = 0
    hero = 0
    font = pygame.font.SysFont(None, 48)
    back_btn = font.render('<BACK', True, (66, 66, 66))
    save_name_btn = font.render('SAVE NAME', True, (66, 66, 66))
    username_btn = font.render('USERNAME', True, (66, 66, 66))
    hero_btn = font.render('HERO', True, (66, 66, 66))
    start_btn = font.render('START GAME', True, (66, 66, 66))
    active_btns = [font.render('<BACK', True, (123, 123, 123)),
                   font.render('SAVE NAME:', True, (123, 123, 123)),
                   font.render('USERNAME:', True, (123, 123, 123)),
                   font.render('HERO:', True, (123, 123, 123)),
                   font.render('START GAME>', True, (123, 123, 123))]

    knight = font.render('knight', True, (66, 66, 66))
    knight_active = font.render('knight', True, (123, 123, 123))
    archer = font.render('archer', True, (66, 66, 66))
    archer_active = font.render('archer', True, (123, 123, 123))

    save_name = 'unnamed_save'
    username = 'no_name'

    new_running = True
    while new_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if selection == 0:
                        new_running = False
                    elif selection == 3:
                        hero = (hero + 1) % 2
                    elif selection == 4:
                        if hero:
                            return [1, hero, 125, 10, 2, 0, username, save_name]
                        return [0, hero, 250, 10, 4, 0, username, save_name]
                elif event.key == pygame.K_UP and selection > 0:
                    selection -= 1
                elif event.key == pygame.K_DOWN and selection < 4:
                    selection += 1
                else:
                    if selection == 1:
                        if event.key == pygame.K_BACKSPACE and save_name:
                            save_name = save_name[:-1]
                        elif event.key != pygame.K_BACKSPACE:
                            save_name += event.unicode
                    elif selection == 2:
                        if event.key == pygame.K_BACKSPACE and username:
                            username = username[:-1]
                        elif event.key != pygame.K_BACKSPACE:
                            username += event.unicode
        screen.fill((0, 0, 0))
        screen.blit(back_btn, (20, 20))
        screen.blit(save_name_btn, (20, 120))
        screen.blit(username_btn, (20, 220))
        screen.blit(hero_btn, (20, 320))
        screen.blit(start_btn, (20, 420))
        screen.blit(active_btns[selection], (20, 100 * selection + 20))

        if hero:
            screen.blit(knight, (320, 320))
            screen.blit(archer_active, (520, 320))
        else:
            screen.blit(knight_active, (320, 320))
            screen.blit(archer, (520, 320))

        save_name_ed = font.render(save_name, True, (66, 66, 66))
        username_ed = font.render(username, True, (66, 66, 66))
        if selection == 1:
            save_name_ed = font.render(save_name, True, (123, 123, 123))
        elif selection == 2:
            username_ed = font.render(username, True, (123, 123, 123))

        screen.blit(save_name_ed, (320, 120))
        screen.blit(username_ed, (320, 220))

        pygame.display.flip()


def load_game(screen):
    selection = 0
    font = pygame.font.SysFont(None, 48)
    back_btn = font.render('<BACK', True, (66, 66, 66))
    back_btn_active = font.render('<BACK', True, (123, 123, 123))

    with open('data/saves/saves_data.json') as f:
        saves = json.load(f)
    f.close()

    load_running = True
    while load_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and selection < len(saves):
                    selection += 1
                elif event.key == pygame.K_UP and selection > 0:
                    selection -= 1
                elif event.key == pygame.K_SPACE:
                    if selection == 0:
                        load_running = False
                    else:
                        save = []
                        with open(f'data/saves/{saves[selection - 1]}.json') as f:
                            data = json.load(f)
                            for key, value in data.items():
                                save.append(value)
                        f.close()
                        return save + [saves[selection - 1]]

        screen.fill((0, 0, 0))
        for i in range(len(saves)):
            screen.blit(font.render(saves[i], True, (66, 66, 66)),
                        (20, 50 * (i + 1) + 30))
        screen.blit(back_btn, (20, 20))
        if selection == 0:
            screen.blit(back_btn_active, (20, 20))
        else:
            screen.blit(font.render(saves[selection - 1], True, (123, 123, 123)),
                        (20, 50 * selection + 30))

        pygame.display.flip()


def leaders(screen):
    font = pygame.font.SysFont(None, 48)
    back_btn = font.render('<BACK', True, (123, 123, 123))
    screen.fill((0, 0, 0))
    screen.blit(back_btn, (20, 20))
    with open('data/leaderboard.json') as f:
        table = json.load(f)
    f.close()
    for i in range(len(table)):
        key = list(table.keys())[i]
        screen.blit(font.render(f'{str(table[key])[:4]}        {key}',
                                True, (212, 212, 212)), (20, 50 * (i + 1) + 30))
    pygame.display.flip()

    leaders_running = True
    while leaders_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    leaders_running = False


def ending(screen, score, hero):
    font = pygame.font.SysFont(None, 48)
    back_btn = font.render('<BACK', True, (123, 123, 123))
    screen.fill((0, 0, 0))
    screen.blit(back_btn, (20, 20))
    screen.blit(font.render('TOTAL SCORE:', True, (66, 66, 66)), (20, 120))
    if hero:
        screen.blit(font.render(str(score / 500)[:4] + '    (archer)', True, (66, 66, 66)), (20, 150))
    else:
        screen.blit(font.render(str(score / 1000)[:4] + '    (knight)', True, (66, 66, 66)), (20, 150))
    pygame.display.flip()

    ending_running = True
    while ending_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ending_running = False
