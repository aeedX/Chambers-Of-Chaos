from stuff import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Chambers Of Chaos')
    size = width, height = 1088, 640
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 20
    running = True
    player = Player()
    level = Level()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                player.action(event)
        screen.fill((255, 255, 255))
        player.update()
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
