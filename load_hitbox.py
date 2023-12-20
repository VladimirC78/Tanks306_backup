import random

import numpy as np
import pygame

import Levels_encoded
import objects

map_number = len(Levels_encoded.fields)


def calculate_distance(place1, place2):
    # Рассчитывает расстояние между двумя объектами, например, между танком и стеной
    return place1[0] - place2[0], place1[1] - place2[1]


def segment_distance(x, y, x1, y1, x2, y2):  # Рассчитывает расстояние между точкой (х, у) и отрезком (х1, у1, х2, у2)
    v1 = np.array([x - x1, y - y1])
    v2 = np.array([x - x2, y - y2])
    v3 = np.array([x2 - x1, y2 - y1])
    v4 = -v3

    prod1 = np.dot(v1, v3)
    prod2 = np.dot(v2, v4)

    if prod1 * prod2 < 0:
        return min(((x - x1) ** 2 + (y - y1) ** 2) ** 0.5, ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5)
    else:
        if x2 != x1:
            k = (y2 - y1) / (x2 - x1)
            b1 = y1 - k * x1
            return abs(y - k * x - b1) / (k ** 2 + 1) ** 0.5
        else:
            return abs(x - x1)


def create_walls(field, block_size):
    # Создает стены
    walls = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                chance = random.choice(range(100))
                if chance <= 20:
                    walls.append(BreakableWall(block_size, (j + 0.5) * block_size, (i + 0.5) * block_size))
                walls.append(Wall(block_size, (j + 0.5) * block_size, (i + 0.5) * block_size))

    return walls


def create_new_map():
    map_choice = random.choice(range(map_number))
    field = Levels_encoded.fields[map_choice]
    scale_factor = 800 // len(field)
    block_size = scale_factor
    walls = create_walls(field, block_size)
    return walls, field, block_size


def check_hit(obj1, obj2):
    x1 = obj1.rect.topleft[0] - obj2.scale
    y1 = obj1.rect.topleft[1] - obj2.scale
    hit_rect = pygame.Rect(x1, y1, obj1.scale + 2 * obj2.scale, obj1.scale + 2 * obj2.scale)
    if hit_rect.collidepoint(obj2.r):
        return True
    else:
        return False


class Wall:
    def __init__(self, block_size, x, y):
        self.block_size = block_size
        self.r = list([x, y])
        self.hit_dict = {'u': False, 'd': False, 'r': False, 'l': False}
        self.rect = pygame.Rect(x - block_size * 0.5, y - block_size * 0.5, block_size, block_size)

    def wall_hit(self, obj):
        # Проверка на соударение объекта со стенкой, принимает на вход параметры объекта
        # Возвращает словарь, указывающий с какой стороны произошло столкновение, нужно использовать
        # в move_draw для изменения скорости танка или пули
        self.hit_dict = {'u': False, 'd': False, 'r': False, 'l': False}
        if isinstance(obj, objects.Bullet):
            top_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] - obj.scale, self.block_size, obj.scale)
            bot_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] + self.block_size, self.block_size,
                                   obj.scale)
            left_rect = pygame.Rect(self.rect.topleft[0] - obj.scale, self.rect.topleft[1], obj.scale, self.block_size)
            right_rect = pygame.Rect(self.rect.topleft[0] + self.block_size, self.rect.topleft[1], 10, self.block_size)
            if left_rect.collidepoint(obj.r):
                self.hit_dict['l'] = True
            if right_rect.collidepoint(obj.r):
                self.hit_dict['r'] = True
            if top_rect.collidepoint(obj.r):
                self.hit_dict['u'] = True
            if bot_rect.collidepoint(obj.r):
                self.hit_dict['d'] = True
        elif isinstance(obj, objects.Tank):
            wall_top_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] - 1, self.block_size, 1)
            wall_bot_rect = pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1], self.block_size, 1)
            wall_left_rect = pygame.Rect(self.rect.topleft[0] - 1, self.rect.topleft[1], 1, self.block_size)
            wall_right_rect = pygame.Rect(self.rect.topright[0], self.rect.topright[1], 1, self.block_size)
            if obj.moving_back:
                tank_top_rect = pygame.Rect(obj.rect.topleft[0], obj.rect.topleft[1] - 5, obj.scale, 10)
                tank_bot_rect = pygame.Rect(obj.rect.topleft[0], obj.rect.bottomleft[1] - 5, obj.scale, 10)
                tank_left_rect = pygame.Rect(obj.rect.topleft[0] - 5, obj.rect.topleft[1], 10, obj.scale)
                tank_right_rect = pygame.Rect(obj.rect.topright[0] - 5, obj.rect.topright[1], 10, obj.scale)
            else:
                tank_top_rect = pygame.Rect(obj.rect.topleft[0], obj.rect.topleft[1], obj.scale, 1)
                tank_bot_rect = pygame.Rect(obj.rect.topleft[0], obj.rect.bottomleft[1] - 1, obj.scale, 1)
                tank_left_rect = pygame.Rect(obj.rect.topleft[0], obj.rect.topleft[1], 1, obj.scale)
                tank_right_rect = pygame.Rect(obj.rect.topright[0] - 1, obj.rect.topright[1], 1, obj.scale)

            if wall_top_rect.colliderect(tank_bot_rect):
                self.hit_dict['u'] = True
            if wall_bot_rect.colliderect(tank_top_rect):
                self.hit_dict['d'] = True
            if wall_right_rect.colliderect(tank_left_rect):
                self.hit_dict['r'] = True
            if wall_left_rect.colliderect(tank_right_rect):
                self.hit_dict['l'] = True
        return self.hit_dict


class BreakableWall(Wall):
    def __init__(self, block_size, x, y):
        self.block_size = block_size
        self.r = list([x, y])
        self.hit_dict = {'u': False, 'd': False, 'r': False, 'l': False}
        self.rect = pygame.Rect(x - block_size * 0.5, y - block_size * 0.5, block_size, block_size)
        self.hp = 2
