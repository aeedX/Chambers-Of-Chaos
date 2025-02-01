import stuff
from stuff import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Chambers Of Chaos')
    size = width, height = 1088, 704
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 24
    ANIMATIONTICK = pygame.USEREVENT + 1
    DAMAGE = pygame.USEREVENT + 2
    pygame.time.set_timer(ANIMATIONTICK, 60)
    pygame.time.set_timer(DAMAGE, 100)
    running = True
    player = Player()
    level = Level()
    while running:
        for event in pygame.event.get():
            stuff.gl_event = event
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ANIMATIONTICK:
                update_sprites()
            else:
                player.action(event)
        screen.fill((69, 69, 69))
        player.update()
        tiles_group.draw(screen)
        enemies_group.draw(screen)
        player_group.draw(screen)
        pygame.draw.circle(screen, (0, 0, 0), (player.x, player.y), 3)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
