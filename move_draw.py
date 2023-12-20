
"""Этот файл отвечает за изменение координат и отрисовку всех игровых объектов кроме стен"""

from load_hitbox import *
import math
import numpy as np

"""Функция, передвигающая пулю, принимает на вход данные о пуле и стенах карты"""


def bullet_move(obj, walls):
    for wall in walls:
        hit_dict = wall.wall_hit(obj)
        if hit_dict['l'] or hit_dict['r'] or hit_dict['u'] or hit_dict['d']:
            obj.life -= 1

        # Изменение скорости пули в зависимости от стороны, с которой она налетает на стену

        if hit_dict["l"]:
            obj.v[0] *= -1
            obj.r[0] = wall.r[0] - wall.block_size * 0.6 - obj.scale
        elif hit_dict["r"]:
            obj.v[0] *= -1
            obj.r[0] = wall.r[0] + wall.block_size * 0.6 + obj.scale
        if hit_dict["u"]:
            obj.v[1] *= -1
            obj.r[1] = wall.r[1] - wall.block_size * 0.6 - obj.scale
        elif hit_dict["d"]:
            obj.v[1] *= -1
            obj.r[1] = wall.r[1] + wall.block_size * 0.6 + obj.scale

    obj.r[0] += obj.v[0]
    obj.r[1] += obj.v[1]


"""Отрисовка пули"""


def bullet_draw(screen, color, obj):
    pygame.draw.circle(screen, color, (obj.r[0], obj.r[1]), obj.scale)


"""Отрисовка бонуса, принимает на вход данные бонуса и набор картинок бонусов"""


def draw_bonus(screen, obj, imgs):
    if obj.var == 'LASER':
        screen.blit(imgs[2], (obj.r[0] - 17, obj.r[1] - 6))
    elif obj.var == 'TRIPLESHOT':
        screen.blit(imgs[1], (obj.r[0] - 19, obj.r[1] - 10))
    elif obj.var == 'SHIELD':
        screen.blit(imgs[0], (obj.r[0] - 20, obj.r[1] - 20))


"""Отрисовка лазеров, изображает их в виде толстого луча заданного цвета"""


def draw_laser(screen, obj, color):
    col = color
    pygame.draw.line(screen, col, [obj.r[0], obj.r[1]], [obj.end[0], obj.end[1]], obj.width)


"""Вращение картинки танка, принимает на вход картинку, связанный с ней прямоугольник и угол поворота, 
возвращает повернутую картинку и связанный с ней прямоугольник"""


def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


"""Отрисовка танка в зависимости от угла поворота, использует данные из функции выше"""


def draw_tank(obj, screen):
    image = pygame.transform.scale(pygame.image.load('graphics/tank_alt.png'), (obj.scale, obj.scale))
    rect = image.get_rect(center=(obj.r[0], obj.r[1]))
    surf, r = rot_center(image, rect, obj.ang * 180 / math.pi)
    screen.blit(surf, r)
    return rect


"""Изменение координат танка в зависимости от угла поворота. Косвенно учитываются стены через параметры vx и vy"""


def move_tank(obj, vx, vy):
    if obj.moving_front:
        obj.v = [-vx * np.sin(obj.ang), -vy * np.cos(obj.ang)]
    elif obj.moving_back:
        obj.v = [vx * np.sin(obj.ang), vy * np.cos(obj.ang)]

    if obj.turning_left:
        obj.ang += obj.omega
    if obj.turning_right:
        obj.ang -= obj.omega

    if not obj.moving_front and not obj.moving_back:
        obj.v = [0, 0]

    obj.r[0] += obj.v[0]
    obj.r[1] += obj.v[1]
