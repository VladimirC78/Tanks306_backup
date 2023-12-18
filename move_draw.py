# TODO здесь нужно написать функции, меняющие координаты объектов, а так же рисующие их
import pygame
import numpy as np
from load_hitbox import *


def bullet_move(obj, walls):
    obj.r[0] += obj.v[0]  # вроде бы v- это вектор, поэтому беру проекцию
    obj.r[1] += obj.v[1]
    # for wall in walls:
    #     if wall.wall_hit(obj)["l"]:
    #         obj.v[0] *= -1
    #     elif wall.wall_hit(obj)["r"]:
    #         obj.v[0] *= -1
    #     if wall.wall_hit(obj)["u"]:
    #         obj.v[1] *= -1
    #     elif wall.wall_hit(obj)["d"]:
    #         obj.v[1] *= -1
    """Пока вот так прописала условие столкновения пули и стены. НО есть риск, что пуля будет застревать на стенах
        , как тогда в пушке, если дополнительно пулю не отдалить от стены, но это уже нужно сделать после того,
       как игра сможет запуститься """


def motion_up(obj,
              walls):  # движение вверх с учетом столкновения танка со стенами в карте(у танка теперь есть свой словарь)
    if obj.tank_check_hit(walls)["l"]:
        if np.sin(obj.ang) <= 0:
            obj.r[0] -= obj.v * np.sin(obj.ang)
    if obj.tank_check_hit(walls)["r"]:
        if np.sin(obj.ang) >= 0:
            obj.r[0] -= obj.v * np.sin(obj.ang)
    if (obj.tank_check_hit(walls)["r"] == obj.tank_check_hit(walls)["l"]) and obj.tank_check_hit(walls)["r"] == False:
        obj.r[0] -= obj.v * np.sin(obj.ang)
    if obj.tank_check_hit(walls)["u"]:
        if np.cos(obj.ang) <= 0:
            obj.r[1] -= obj.v * np.cos(obj.ang)
    if obj.tank_check_hit(walls)["d"]:
        if np.cos(obj.ang) >= 0:
            obj.r[1] -= obj.v * np.cos(obj.ang)
    if (obj.tank_check_hit(walls)["u"] == obj.tank_check_hit(walls)["d"]) and obj.tank_check_hit(walls)["d"] == False:
        obj.r[1] -= obj.v * np.cos(obj.ang)


def motion_down(obj, walls):
    if obj.tank_check_hit(walls)["l"]:
        if np.sin(obj.ang) >= 0:
            obj.r[0] += obj.v * np.sin(obj.ang)
    if obj.tank_check_hit(walls)["r"]:
        if np.sin(obj.ang) <= 0:
            obj.r[0] += obj.v * np.sin(obj.ang)
    if (obj.tank_check_hit(walls)["r"] == obj.tank_check_hit(walls)["l"]) and not obj.tank_check_hit(walls)[
        "r"]:
        obj.r[0] += obj.v * np.sin(obj.ang)

    if obj.tank_check_hit(walls)["u"]:
        if np.cos(obj.ang) >= 0:
            obj.r[1] += obj.v * np.cos(obj.ang)
    if obj.tank_check_hit(walls)["d"]:
        if np.cos(obj.ang) <= 0:
            obj.r[1] += obj.v * np.cos(obj.ang)
    if (obj.tank_check_hit(walls)["u"] == obj.tank_check_hit(walls)["d"]) and not obj.tank_check_hit(walls)[
        "d"]:
        obj.r[1] += obj.v * np.cos(obj.ang)


def tank_move(obj, walls):
    keys = pygame.key.get_pressed()

    if obj.type == 1:
        if keys[pygame.K_w]:
            motion_up(obj, walls)
        elif keys[pygame.K_s]:
            motion_down(obj, walls)

        if keys[pygame.K_a]:
            obj.ang += obj.omega
        elif keys[pygame.K_d]:
            obj.ang -= obj.omega
    else:
        if keys[pygame.K_UP]:
            motion_up(obj, walls)
        elif keys[pygame.K_DOWN]:
            motion_down(obj, walls)

        if keys[pygame.K_LEFT]:
            obj.ang += obj.omega
        elif keys[pygame.K_RIGHT]:
            obj.ang -= obj.omega


"""Итог работы: пришлось писать для танка свой словарь столкновений: если он контачит, например, слева, хоть с одной стеной,
то в соответсвующем ключе у словаря будет значение True. Думаю, лучше это прописать в классе танка, чем прямо здесь
писать цикл проверки столкновения танка со стенами. Чтобы проверить столкновение, обращаюсь к словарю столкновений, он будет 
пересчитываться постоянно во время работы программы.С пулей все проще, можно прям в функции написать цикл проверки столновений.
Вынесла повторяющийся код в функции "motion_up" и "motion_down" """
