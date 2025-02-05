import pygame

import stuff
from screens import start_screen, ending, terminate
from stuff import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Chambers Of Chaos')
    size = width, height = 1088, 704
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 24

    font = pygame.font.SysFont(None, 48)
    next_lvl_tip = font.render('press ENTER for next lvl', True, (123, 123, 123))

    ANIMATIONTICK = pygame.USEREVENT + 1
    DAMAGE = pygame.USEREVENT + 2
    pygame.time.set_timer(ANIMATIONTICK, 60)
    pygame.time.set_timer(DAMAGE, 1)
    Border(0, 64, width, 64)
    Border(0, height - 64 - 64, width, height - 64 - 64)
    Border(64, 0, 64, height)
    Border(width - 64, 0, width - 64, height)
    Border(0, 62, width, 62)
    Border(0, height - 64 - 62, width, height - 64 - 62)
    Border(62, 0, 62, height)
    Border(width - 62, 0, width - 62, height)
    Border(0, 60, width, 60)
    Border(0, height - 64 - 60, width, height - 64 - 60)
    Border(60, 0, 60, height)
    Border(width - 60, 0, width - 60, height)
    Border(0, 58, width, 58)
    Border(0, height - 64 - 58, width, height - 64 - 58)
    Border(58, 0, 58, height)
    Border(width - 58, 0, width - 58, height)

    def main():
        player, level, username, save_name = start_screen(screen)
        save(save_name, username, player, level)

        health = font.render('HP:', True, (66, 66, 66))
        damage = font.render('DAMAGE:', True, (66, 66, 66))
        speed = font.render('SPEED:', True, (66, 66, 66))

        running = True
        while running:
            for event in pygame.event.get():
                stuff.gl_event = event
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == ANIMATIONTICK:
                    update_sprites()
                else:
                    player.action(event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and not enemies_group.sprites():
                            arrow_group.empty()
                            level.lvl_id += 1
                            player.score += player.hp
                            if level.lvl_id < 4:
                                level.load_level()
                            else:
                                running = False
                            save(save_name, username, player, level)
            if not player_group.sprites():
                save(save_name, username, player, level)
                running = False
            screen.fill((0, 0, 0))
            player.update()
            arrow_group.update()
            enemies_group.update()
            tiles_group.draw(screen)
            enemies_group.draw(screen)
            player_group.draw(screen)
            arrow_group.draw(screen)

            screen.blit(health, (20, 656))
            screen.blit(damage, (240, 656))
            screen.blit(speed, (480 , 656))

            health_ed = font.render(f'{int(player.hp)}/{int(player.max_hp)}', True, (123, 123, 123))
            damage_ed = font.render(str(player.damage), True, (123, 123, 123))
            speed_ed = font.render(str(player.speed), True, (123, 123, 123))
            screen.blit(health_ed, (80, 656))
            screen.blit(damage_ed, (405, 656))
            screen.blit(speed_ed, (605, 656))
            if not enemies_group.sprites():
                screen.blit(next_lvl_tip, (680, 656))
            clock.tick(fps)
            pygame.display.flip()
        ending(screen, player.score, player.hero)

    while True:
        main()
