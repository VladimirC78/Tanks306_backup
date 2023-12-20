import pygame
import math


class Tank:
    def __init__(self, x, y, scale, type):
        self.type = type
        self.r = list([x, y])  # Координаты танка по осям х и у
        self.scale = scale  # Характерный размер танка
        self.v = [0, 0]  # Вектор скорости
        self.omega = 0.02
        self.ang = 0  # Изначально танк направлен вправо, угол в радианах и отсчитывается по часовой стрелке
        self.charges = 5
        self.tank_hit_walls = {'u': False, 'd': False, 'r': False, 'l': False}
        self.live = 1  # жизнь танка
        self.rect = pygame.Rect(self.r[0] - self.scale * 0.5, self.r[1] - self.scale * 0.5, self.scale, self.scale)
        self.moving_front = False
        self.moving_back = False
        self.turning_left = False
        self.turning_right = False


class Bullet:
    def __init__(self, x, y, v, scale):
        self.r = list([x, y])  # Координаты танка по осям х и у
        self.scale = scale  # Радиус пули
        self.v = v  # Двумерный вектор со скоростями по осям
        self.life = 2

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (self.r[0], self.r[1]), self.scale)
