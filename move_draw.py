# TODO здесь нужно написать функции, меняющие координаты объектов, а так же рисующие их
import pygame
import numpy as np
from load_hitbox import *


def bullet_move(obj, walls):
    for wall in walls:
        hit_dict = wall.wall_hit(obj)
        if hit_dict['l'] or hit_dict['r'] or hit_dict['u'] or hit_dict['d']:
            obj.life -= 1
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
    """Пока вот так прописала условие столкновения пули и стены. НО есть риск, что пуля будет застревать на стенах
        , как тогда в пушке, если дополнительно пулю не отдалить от стены, но это уже нужно сделать после того,
       как игра сможет запуститься """


# def motion_up(obj,
#               walls):  # движение вверх с учетом столкновения танка со стенами в карте(у танка теперь есть свой словарь)
#     if obj.tank_check_hit(walls)["l"]:
#         if np.sin(obj.ang) <= 0:
#             obj.r[0] -= obj.v * np.sin(obj.ang)
#     if obj.tank_check_hit(walls)["r"]:
#         if np.sin(obj.ang) >= 0:
#             obj.r[0] -= obj.v * np.sin(obj.ang)
#     if (obj.tank_check_hit(walls)["r"] == obj.tank_check_hit(walls)["l"]) and obj.tank_check_hit(walls)["r"] == False:
#         obj.r[0] -= obj.v * np.sin(obj.ang)
#     if obj.tank_check_hit(walls)["u"]:
#         if np.cos(obj.ang) <= 0:
#             obj.r[1] -= obj.v * np.cos(obj.ang)
#     if obj.tank_check_hit(walls)["d"]:
#         if np.cos(obj.ang) >= 0:
#             obj.r[1] -= obj.v * np.cos(obj.ang)
#     if (obj.tank_check_hit(walls)["u"] == obj.tank_check_hit(walls)["d"]) and obj.tank_check_hit(walls)["d"] == False:
#         obj.r[1] -= obj.v * np.cos(obj.ang)


# def motion_down(obj, walls):
#     if obj.tank_check_hit(walls)["l"]:
#         if np.sin(obj.ang) >= 0:
#             obj.r[0] += obj.v * np.sin(obj.ang)
#     if obj.tank_check_hit(walls)["r"]:
#         if np.sin(obj.ang) <= 0:
#             obj.r[0] += obj.v * np.sin(obj.ang)
#     if (obj.tank_check_hit(walls)["r"] == obj.tank_check_hit(walls)["l"]) and not obj.tank_check_hit(walls)[
#         "r"]:
#         obj.r[0] += obj.v * np.sin(obj.ang)
#
#     if obj.tank_check_hit(walls)["u"]:
#         if np.cos(obj.ang) >= 0:
#             obj.r[1] += obj.v * np.cos(obj.ang)
#     if obj.tank_check_hit(walls)["d"]:
#         if np.cos(obj.ang) <= 0:
#             obj.r[1] += obj.v * np.cos(obj.ang)
#     if (obj.tank_check_hit(walls)["u"] == obj.tank_check_hit(walls)["d"]) and not obj.tank_check_hit(walls)[
#         "d"]:
#         obj.r[1] += obj.v * np.cos(obj.ang)


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


# def tank_move(obj, walls):
#     keys = pygame.key.get_pressed()
#
#     if obj.type == 1:
#         if keys[pygame.K_w]:
#             motion_up(obj, walls)
#         elif keys[pygame.K_s]:
#             motion_down(obj, walls)
#
#         if keys[pygame.K_a]:
#             obj.ang += obj.omega
#         elif keys[pygame.K_d]:
#             obj.ang -= obj.omega
#     else:
#         if keys[pygame.K_UP]:
#             motion_up(obj, walls)
#         elif keys[pygame.K_DOWN]:
#             motion_down(obj, walls)
#
#         if keys[pygame.K_LEFT]:
#             obj.ang += obj.omega
#         elif keys[pygame.K_RIGHT]:
#             obj.ang -= obj.omega


"""Итог работы: пришлось писать для танка свой словарь столкновений: если он контачит, например, слева, хоть с одной стеной,
то в соответсвующем ключе у словаря будет значение True. Думаю, лучше это прописать в классе танка, чем прямо здесь
писать цикл проверки столкновения танка со стенами. Чтобы проверить столкновение, обращаюсь к словарю столкновений, он будет 
пересчитываться постоянно во время работы программы.С пулей все проще, можно прям в функции написать цикл проверки столновений.
Вынесла повторяющийся код в функции "motion_up" и "motion_down" """
