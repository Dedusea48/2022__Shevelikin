import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill('grey')

circle(screen, (255, 255, 0), (200, 175), 100)
circle(screen, (0, 0, 0), (200, 175), 100, 1)
rect(screen, (0, 0, 0), (150, 230, 100, 20))

circle(screen, (255, 0, 0), (150, 150), 20)
circle(screen, (0, 0, 0), (150, 150), 20, 1)
circle(screen, (0, 0, 0), (150, 150), 10)

circle(screen, (255, 0, 0), (250, 150), 18)
circle(screen, (0, 0, 0), (250, 150), 18, 1)
circle(screen, (0, 0, 0), (250, 150), 8)

polygon(screen, (0, 0, 0), [(100, 100), (200, 140),
                            (195, 145), (95, 105)])
polygon(screen, (0, 0, 0), [(280, 100), (210, 140),
                            (215, 145), (285, 105)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
