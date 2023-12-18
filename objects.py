import pygame
import math


def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


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

    # def tank_check_hit(self, walls):
    #     l, r, u, d = False, False, False, False
    #     for wall in walls:
    #         if wall.wall_hit(self)["l"]:
    #             l = True
    #         if wall.wall_hit(self)["r"]:
    #             r = True
    #         if wall.wall_hit(self)["u"]:
    #             u = True
    #         if wall.wall_hit(self)["d"]:
    #             d = True
    #     self.tank_hit_walls = {'u': u, 'd': d, 'r': r, 'l': l}
    #     return self.tank_hit_walls

        # Количество выстрелов у танка, перезаряжается со временем

    def draw(self, screen):
        image = pygame.transform.scale(pygame.image.load('tank_alt.png'), (self.scale, self.scale))
        rect = image.get_rect(center=(self.r[0], self.r[1]))
        surf, r = rot_center(image, rect, self.ang * 180 / math.pi)
        screen.blit(surf, r)
        return rect


class Bullet:
    def __init__(self, x, y, v, scale):
        self.r = list([x, y])  # Координаты танка по осям х и у
        self.scale = scale  # Радиус пули
        self.v = v  # Двумерный вектор со скоростями по осям
        self.life = 2

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.r[0], self.r[1]), self.scale)

# TODO Возможно, в процессе нужно будет добавить еще какие-то параметры
