import pygame
from pygame.draw import *


def draw_ellipse_angle(surface, color, rect, angle, width):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    if width != 0:
        pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    else:
        pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size))

    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center=target_rect.center))


pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 1000))
screen.fill((175, 221, 233))

polygon(screen, (100, 100, 100), [(0, 400), (200, 50),
                                  (300, 300), (500, 150),
                                  (700, 600), (820, 320),
                                  (1000, 500), (1000, 1000), (0, 1000)])
polygon(screen, (100, 250, 100), [(0, 700), (450, 700),
                                  (450, 720), (470, 720),
                                  (470, 760), (500, 760),
                                  (500, 790),
                                  (1000, 790), (1000, 1000), (0, 1000)])

circle(screen, (100, 250, 100), (450, 720), 20)
circle(screen, (100, 100, 100), (500, 760), 29)

pygame.draw.ellipse(screen, (255, 255, 255), (100, 670, 100, 40))
pygame.draw.ellipse(screen, (255, 255, 255), (100, 680, 20, 80))
pygame.draw.ellipse(screen, (255, 255, 255), (180, 680, 20, 80))
pygame.draw.ellipse(screen, (255, 255, 255), (190, 610, 20, 80))
circle(screen, (255, 255, 255), (210, 610), 13)
circle(screen, (222, 125, 247), (214, 608), 6)
circle(screen, (0, 0, 0), (216, 607), 2)
polygon(screen, (0, 0, 0), [(200, 600), (190, 590), (195, 610)])
draw_ellipse_angle(screen, (255, 255, 255), (80, 730, 20, 80), 315, 0)
draw_ellipse_angle(screen, (255, 255, 255), (160, 730, 20, 80), 315, 0)

circle(screen, (113, 200, 55), (750, 750), 60)
draw_ellipse_angle(screen, (255, 255, 255), (720, 720, 17, 10), 45, 0)
draw_ellipse_angle(screen, (0, 0, 0), (720, 720, 17, 10), 45, 1)
draw_ellipse_angle(screen, (255, 255, 255), (720, 700, 17, 10), 45, 0)
draw_ellipse_angle(screen, (0, 0, 0), (720, 700, 17, 10), 45, 1)
draw_ellipse_angle(screen, (255, 255, 255), (710, 710, 17, 10), 45, 0)
draw_ellipse_angle(screen, (0, 0, 0), (710, 710, 17, 10), 45, 1)
draw_ellipse_angle(screen, (255, 255, 255), (730, 710, 17, 10), 45, 0)
draw_ellipse_angle(screen, (0, 0, 0), (730, 710, 17, 10), 45, 1)
draw_ellipse_angle(screen, (255, 255, 255), (710, 720, 17, 10), 45, 0)
draw_ellipse_angle(screen, (0, 0, 0), (710, 720, 17, 10), 45, 1)
draw_ellipse_angle(screen, (255, 255, 255), (730, 700, 17, 10), 45, 0)
draw_ellipse_angle(screen, (0, 0, 0), (730, 700, 17, 10), 45, 1)
draw_ellipse_angle(screen, (255, 255, 0), (718, 710, 20, 10), 45, 0)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
