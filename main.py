import stuff
from stuff import *
print(123)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Chambers Of Chaos')
    size = width, height = 1088, 704
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 24

    font = pygame.font.SysFont(None, 48)
    next_lvl_tip = font.render('press ENTER for next lvl', True, (0, 0, 0))

    ANIMATIONTICK = pygame.USEREVENT + 1
    DAMAGE = pygame.USEREVENT + 2
    pygame.time.set_timer(ANIMATIONTICK, 60)
    pygame.time.set_timer(DAMAGE, 1)
    running = True
    player = Player()
    level = Level()
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
    while running:
        for event in pygame.event.get():
            stuff.gl_event = event
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ANIMATIONTICK:
                update_sprites()
                for i in arrow_group:
                    i.update()
                for i in enemies_group:
                    i.update()
            else:
                player.action(event)
        if not enemies_group.sprites():
            arrow_group.empty()
            if level.lvl_id < 3:
                pass
                #level.lvl_id += 1
                #level.load_level()
            else:
                pass
                #game end
        screen.fill((69, 69, 69))
        player.update()
        tiles_group.draw(screen)
        enemies_group.draw(screen)
        player_group.draw(screen)
        arrow_group.draw(screen)
        for i in borders_group:
            i.draw(screen)
        pygame.draw.circle(screen, (0, 0, 0), (player.x, player.y), 3)

        health = font.render(str(int(player.hp)), True, (0, 0, 0))
        max_health = font.render(str(int(player.max_hp)), True, (0, 0, 0))
        damage = font.render(str(player.damage), True, (0, 0, 0))
        speed = font.render(str(player.speed), True, (0, 0, 0))
        screen.blit(health, (50, 656))
        screen.blit(max_health, (150, 656))
        screen.blit(damage, (250, 656))
        screen.blit(speed, (350, 656))
        if not enemies_group.sprites():
            screen.blit(next_lvl_tip, (600, 656))
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
