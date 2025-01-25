import pygame
from stuff import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Chambers Of Chaos')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 20
    running = True
    player = Player()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                player.action(event)
        screen.fill((255, 255, 255))
        player.update()
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
