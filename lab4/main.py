import pygame
import numpy as np
from pygame.draw import *
from random import randint

pygame.init()

HEIGHT = 1000
WIDTH = 1920
N = 9  # Количесво шаров
FPS = 60
COUNTER = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, (255, 102, 0), (102, 102, 153), (255, 153, 0), (255, 153, 204),
          (204, 255, 204)]


class Player:

    def __init__(self):
        self.point = 0

    def add_points(self, points):
        self.point += points

    def pick_up_points(self, points):
        self.point -= points

    def points(self):
        return self.point


class Element:
    x: float
    y: float
    v_x: float
    v_y: float
    r: float
    rx: float
    ry: float
    color: str
    kind: str
    time_of_life = 1

    def __init__(self):
        create(self)

    def moving(self):
        """проверяет шарик на соудорение со стеной или баги и проверка времени жизни"""
        t = 0.5
        self.x += t * self.v_x
        self.y += t * self.v_y
        self.rx = self.r * (1 - np.sin(self.time_of_life * 180 / np.pi) / 4)
        self.ry = self.r * (1 + np.sin(self.time_of_life * 180 / np.pi) / 4)
        if self.kind == "ball":
            if self.x <= self.r:
                self.x = self.r
                self.v_x = randint(1, 20)
            if self.x >= WIDTH - self.r:
                self.x = WIDTH - self.r
                self.v_x = randint(-20, -1)
            if self.y < self.r:
                self.y = self.r
                self.v_y = randint(1, 20)
            if self.y >= HEIGHT - self.r:
                self.y = HEIGHT - self.r
                self.v_y = randint(-20, -1)
        if self.kind == "ellipse":
            self.time_of_life -= 0.001
            if self.x <= self.rx:
                self.x = self.rx
                self.v_x = - self.v_x
            if self.x >= WIDTH - self.rx:
                self.x = WIDTH - self.rx
                self.v_x = - self.v_x
            if self.y <= self.ry:
                self.y = self.ry
                self.v_y = -self.v_y
            if self.y >= HEIGHT - self.ry:
                self.y = HEIGHT - self.ry
                self.v_y = -self.v_y
        if self.time_of_life <= 0:
            create(self)
            self.time_of_life = 1

    def rendering(self):
        if self.kind == "ball":
            circle(screen, self.color, (self.x, self.y), self.r)
        elif self.kind == "ellipse":
            ellipse(screen, self.color, (self.x - self.rx, self.y - self.ry, 2 * self.rx, 2 * self.ry))

    def points(self, player):
        if self.kind == "ball":
            if abs(event.pos[1] - self.y) < self.r and abs(event.pos[0] - self.x) < self.r:
                player.add_points(1)
                create(self)

        if self.kind == "ellipse":
            c: float = abs(self.rx ** 2 - self.ry ** 2) ** 0.5
            if self.rx >= self.ry:
                F1: float = self.x - c
                F2: float = self.x + c
                F: float = self.y
                if ((event.pos[1] - F) ** 2 + (event.pos[0] - F2) ** 2) ** 0.5 + (
                        (event.pos[1] - F) ** 2 + (event.pos[0] - F1) ** 2) ** 0.5 <= 2 * self.rx:
                    player.add_points(5)
                    create(self)
            else:
                F1: float = self.y - c
                F2: float = self.y + c
                F: float = self.x
                if ((event.pos[0] - F) ** 2 + (event.pos[1] - F2) ** 2) ** 0.5 + (
                        (event.pos[0] - F) ** 2 + (event.pos[1] - F1) ** 2) ** 0.5 <= 2 * self.ry:
                    player.add_points(5)
                    create(self)


def create(element):
    """
    :param element: create element
    code:
    element.x = randint(0, WIDTH)
    element.y = randint(0, HEIGHT)
    element.v_x = randint(-20, 20)
    element.v_y = randint(-20, 20)
    element.r = randint(20, 100)
    if randint(1, 3) == 1:
        element.kind = "ellipse"
        element.color = COLORS[randint(6, 10)]
    else:
        element.kind = "ball"
        element.color = COLORS[randint(0, 5)]
    """
    element.x = randint(0, WIDTH)
    element.y = randint(0, HEIGHT)
    element.v_x = randint(-20, 20)
    element.v_y = randint(-20, 20)
    element.r = randint(20, 100)
    if randint(1, 3) == 1:
        element.kind = "ellipse"
        element.color = COLORS[randint(6, 10)]
    else:
        element.kind = "ball"
        element.color = COLORS[randint(0, 5)]


pygame.display.update()
clock = pygame.time.Clock()
finished = False
A = []
Max = Player()

for i in range(N):
    A.append(Element())

while not finished:
    clock.tick(FPS)

    for i in range(N):
        A[i].moving()
        A[i].rendering()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(N):
                A[i].points(Max)
    pygame.display.update()
    screen.fill(BLACK)
print(Max.points())
pygame.quit()
