import math
from random import choice
from random import randint as rnd

import numpy
import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
LIME = (158, 253, 56)
GAME_COLORS: list[int] = [LIME, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.y <= HEIGHT - self.r or self.vy != 0:
            self.vy -= 4
        self.x += self.vx
        self.y -= self.vy + 2
        if self.x >= 800 - self.r:
            self.x = 800 - self.r
            self.vx //= -2
            self.vy //= 4
            if self.vy == -2:
                self.vy = 0
        if self.y >= HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy //= -2
            self.vx //= 2
        if abs(self.vx) <= 2:
            self.vx = 0
        if abs(self.vy) <= 2:
            self.vy = 0

    def draw(self):
        """
        отрисовывает шарик
        """
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x) * (self.x - obj.x) + (self.y - obj.y) * (self.y - obj.y)) ** 0.5 <= self.r + obj.r:
            return True
        else:
            return False


class Gun:
    def __init__(self, shield):
        self.screen = shield
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self):
        """
        присваивает f2_power значеие один
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event and (event.pos[0] - 20) != 0:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """
        отрисовывает пушку
        """
        pygame.draw.circle(self.screen, self.color, (40, 450), 20)
        pygame.draw.polygon(self.screen, (int(self.f2_power * 2.55), 0, 0), [(0, 430), (40, 430), (40, 470), (0, 470)])

    def power_up(self):
        """
        увеличивает f2_power на один и меняет цвет конца пушки
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):
        self.x = None
        self.y = None
        self.r = None
        self.color = None
        self.points = 0
        self.live = 1
        self.new_target()
        self.bias = 0

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(400, 750)
        self.y = rnd(190, 410)
        self.r = rnd(8, 50)
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        """отрисовывает цель"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r, 1)

    def move(self):
        """Двигает цель по вертикали"""
        self.bias += 1
        self.y += 4 * (numpy.sin((self.bias + 1) * 0.18 / numpy.pi) - numpy.sin(self.bias * 0.18 / numpy.pi)) * self.r
        if self.bias == 18000:
            self.bias = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
target = []

clock = pygame.time.Clock()
gun = Gun(screen)

for i in range(2):
    target.append(Target())
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for i in range(2):
        target[i].draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for i in range(2):
        target[i].move()

    j = 0
    for b in balls:
        b.move()
        if b.vx == 0 and b.vy <= 4 and b.y == HEIGHT - b.r:
            balls.pop(j)
        j += 1
        for i in range(2):
            if b.hittest(target[i]) and target[i].live:
                target[i].live = 0
                target[i].hit()
                target[i].new_target()
    gun.power_up()

pygame.quit()
