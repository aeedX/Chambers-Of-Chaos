import pygame
from stuff import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Chambers Of Chaos')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 15
    running = True
    player = Player()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        player.update()
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
