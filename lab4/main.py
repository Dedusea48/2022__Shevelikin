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
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN,
          (255, 102, 0), (102, 102, 153), (255, 153, 0), (204, 255, 204), (255, 153, 204)]


class Player:
    def __init__(self):
        self.point: int = 0
        self.name = '000'

    def add_points(self, points):
        """
        Increases the player's score by points
        """
        self.point += points

    def pick_up_points(self, points):
        """Decreases the player's score by points"""
        self.point -= points

    def change_points(self, points):
        self.point = points

    def points(self):
        """
        :return: player's score
        """
        return self.point

    def rename(self):
        """
        code:
        self.name = input()
        """
        self.name = input()

    def say_name(self):
        """
        :return: str(self.name)
        """
        return str(self.name)


class Element:
    x: float
    y: float
    v_x: float
    v_y: float
    r: float = 10
    color: str
    kind: str
    time_of_life = 1
    rx: float = r * (1 - np.sin(time_of_life * 180 / np.pi) / 4)
    ry: float = r * (1 + np.sin(time_of_life * 180 / np.pi) / 4)

    def __init__(self):
        create(self)

    def moving(self):
        """двигает элемент, проверяет на соудорение со стеной или баги и проверка времени жизни"""
        t = 0.5
        self.x += t * self.v_x
        self.y += t * self.v_y
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
            self.rx = self.r * (1 - np.sin(self.time_of_life * 180 / np.pi) / 4)
            self.ry = self.r * (1 + np.sin(self.time_of_life * 180 / np.pi) / 4)
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
        """Отрисовывает элемент"""
        if self.kind == "ball":
            circle(screen, self.color, (self.x, self.y), self.r)
        elif self.kind == "ellipse":
            ellipse(screen, self.color, (self.x - self.rx, self.y - self.ry, 2 * self.rx, 2 * self.ry))

    def click(self, gamer):
        """Проверка попал ли игрок по элементу, добавление очков и создание нового при попадании"""
        if self.kind == "ball":
            if abs(event.pos[1] - self.y) < self.r and abs(event.pos[0] - self.x) < self.r:
                gamer.add_points(1)
                create(self)

        if self.kind == "ellipse":
            c: float = abs(self.rx ** 2 - self.ry ** 2) ** 0.5
            if self.rx >= self.ry:
                if ((event.pos[1] - self.y) ** 2 + (event.pos[0] - self.x - c) ** 2) ** 0.5 + (
                        (event.pos[1] - self.y) ** 2 + (event.pos[0] - self.x + c) ** 2) ** 0.5 <= 2 * self.rx:
                    gamer.add_points(5)
                    create(self)
            else:
                if ((event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y - c) ** 2) ** 0.5 + (
                        (event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y + c) ** 2) ** 0.5 <= 2 * self.ry:
                    gamer.add_points(5)
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


def file_work(gamer, filename):
    names = []
    score = []

    def readfile():
        """
        Reade data by filename, and  write it in name[] and score[]
        """
        f = open(filename, 'r')
        for q in range(5):
            names.append(str(f.readline(3)))
            f.readline()
            score.append(int(f.readline()))
        f.close()

    def rescore():
        """Checks if the old record holder set a new record and if not puts the current player in last place in the ranking if he broke the record holder's record"""
        re_score = False
        for q in range(5):
            if names[q] == gamer.say_name() and gamer.points() > score[q]:
                score[q] = gamer.points()
                names[q] = gamer.say_name()
                re_score = True
        if not re_score and score[4] <= gamer.points():
            score[4] = gamer.points()
            names[4] = gamer.say_name()

    def sort():
        """one piece bubble sort"""
        for q in range(4, 0, -1):
            if score[q] >= score[q - 1]:
                tup = score[q]
                score[q] = score[q - 1]
                score[q - 1] = tup

                tup = names[q]
                names[q] = names[q - 1]
                names[q - 1] = tup

    def writefile():
        """code:
        f = open(filename, 'w')
        for q in range(5):
            f.write(names[q] + "\n")
            f.write(str(score[q]) + "\n")
        """
        f = open(filename, 'w')
        for q in range(5):
            f.write(names[q] + "\n")
            f.write(str(score[q]) + "\n")
        f.close()

    readfile()
    rescore()
    sort()
    writefile()


pygame.display.update()
clock = pygame.time.Clock()
finished = False
A = []
player = Player()

for i in range(N):
    A.append(Element())
start_ticks = pygame.time.get_ticks()
while (pygame.time.get_ticks() - start_ticks) / 1000 < 60 and not finished:
    clock.tick(FPS)

    for i in range(N):
        A[i].moving()
        A[i].rendering()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(N):
                A[i].click(player)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
print("say your nickname of 3 characters:")
player.rename()
file_work(player, 'data.txt')