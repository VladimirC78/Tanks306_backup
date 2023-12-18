import random
import Levels_encoded

import objects
import numpy as np
import math
import pygame

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
                walls.append(Wall(block_size, j * block_size + block_size * 0.5, i * block_size + block_size * 0.5))

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
        dist = calculate_distance(obj.r, self.r)
        top_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] - obj.scale, self.block_size, obj.scale)
        bot_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] + self.block_size, self.block_size, obj.scale)
        left_rect = pygame.Rect(self.rect.topleft[0] - obj.scale, self.rect.topleft[1], obj.scale, self.block_size)
        right_rect = pygame.Rect(self.rect.topleft[0] + self.block_size, self.rect.topleft[1], 10, self.block_size)
        if isinstance(obj, objects.Bullet):
            if left_rect.collidepoint(obj.r):
                self.hit_dict['l'] = True
            if right_rect.collidepoint(obj.r):
                self.hit_dict['r'] = True
            if top_rect.collidepoint(obj.r):
                self.hit_dict['u'] = True
            if bot_rect.collidepoint(obj.r):
                self.hit_dict['d'] = True
        elif isinstance(obj, objects.Tank):
            if pygame.Rect.colliderect(self.rect, obj.rect):
                if 0 < dist[0] <= (self.block_size + obj.scale) * 0.5:
                    self.hit_dict['r'] = True
                if dist[0] < 0 and abs(dist[0]) <= (self.block_size + obj.scale) * 0.5:
                    self.hit_dict['l'] = True
                if dist[1] < 0 and abs(dist[1]) <= (self.block_size + obj.scale) * 0.5:
                    self.hit_dict['u'] = True
                if 0 < dist[1] <= (self.block_size + obj.scale) * 0.5:
                    self.hit_dict['d'] = True
                print(self.hit_dict, self.r, obj.r, dist)
        return self.hit_dict


