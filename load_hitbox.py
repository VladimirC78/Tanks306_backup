import random
import Levels_encoded

import objects
import numpy as np
import math
import pygame

map_number = len(Levels_encoded.fields)


def distance_between_segments(x1, y1, x2, y2, x3, y3, x4, y4):
    def ras(x1, y1, x2, y2, x3, y3):
        # Если отрезок вертикальный - меняем местами координаты каждой точки.
        if x1 == x2:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            x3, y3 = y3, x3
        k = (y1 - y2) / (x1 - x2)  # Ищем коэффициенты уравнения прямой, которому принадлежит данный отрезок.
        d = y1 - k * x1
        xz = (x3 * x2 - x3 * x1 + y2 * y3 - y1 * y3 + y1 * d - y2 * d) / (k * y2 - k * y1 + x2 - x1)
        dl = -1
        if (x2 >= xz >= x1) or (x1 >= xz >= x2):
            dl = math.sqrt((x3 - xz) * (x3 - xz) + (y3 - xz * k - d) * (
                    y3 - xz * k - d))  # Проверим лежит ли основание высоты на отрезке.
        return dl

    # Вводим параметры отрезков
    # xa, ya, xb, yb = [1, 1, 2, 2]
    # xc, yc, xd, yd = [2, 1, 3, 0]

    xa, ya, xb, yb = x1, y1, x2, y2
    xc, yc, xd, yd = x3, y3, x4, y4

    min = -1
    t = -2
    s = -2

    o = (xb - xa) * (-yd + yc) - (yb - ya) * (-xd + xc)
    o1 = (xb - xa) * (yc - ya) - (yb - ya) * (xc - xa)
    o2 = (-yd + yc) * (xc - xa) - (-xd + xc) * (yc - ya)

    if o != 0:
        t = o1 / o
        s = o2 / o

    if (t >= 0 and s >= 0) and (t <= 1 and s <= 1):
        min = 0  # Проверим пересекаются ли отрезки.
    else:
        # Найдём наименьшую высоту опущенную из конца одного отрезка на другой.
        dl1 = ras(xa, ya, xb, yb, xc, yc)
        min = dl1
        dl2 = ras(xa, ya, xb, yb, xd, yd)
        if (dl2 < min and dl2 != -1) or min == -1:
            min = dl2
        dl3 = ras(xc, yc, xd, yd, xa, ya)
        if (dl3 < min and dl3 != -1) or min == -1:
            min = dl3
        dl4 = ras(xc, yc, xd, yd, xb, yb)
        if (dl4 < min and dl4 != -1) or min == -1:
            min = dl4
        if min == -1:
            # В случае, если невозможно опустить высоту найдём минимальное расстояние между точками.
            dl1 = math.sqrt((xa - xc) * (xa - xc) + (ya - yc) * (ya - yc))
            min = dl1
            dl2 = math.sqrt((xb - xd) * (xb - xd) + (yb - yd) * (yb - yd))
            if dl2 < min:
                min = dl2
            dl3 = math.sqrt((xb - xc) * (xb - xc) + (yb - yc) * (yb - yc))
            if dl3 < min:
                min = dl3
            dl4 = math.sqrt((xa - xd) * (xa - xd) + (ya - yd) * (ya - yd))
            if dl4 < min:
                min = dl4

    return min


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


def bullet_hittest(obj1, obj2):  # Проверка попадания пули в танк, здесь obj1 - пуля, obj2 - танк
    # Координаты каждой из вершин танка
    r_a = [obj2.r[0] + 0.5 * obj2.scale * np.cos(np.pi / 4 - obj2.ang),
           obj2.r[1] - 0.5 * obj2.scale * np.sin(np.pi / 4 - obj2.ang)]
    r_c = [obj2.r[0] - 0.5 * obj2.scale * np.cos(np.pi / 4 - obj2.ang),
           obj2.r[1] + 0.5 * obj2.scale * np.sin(np.pi / 4 - obj2.ang)]
    r_b = [obj2.r[0] + 0.5 * obj2.scale * np.cos(np.pi / 4 + obj2.ang),
           obj2.r[1] + 0.5 * obj2.scale * np.sin(np.pi / 4 + obj2.ang)]
    r_d = [obj2.r[0] - 0.5 * obj2.scale * np.cos(np.pi / 4 + obj2.ang),
           obj2.r[1] - 0.5 * obj2.scale * np.sin(np.pi / 4 + obj2.ang)]

    dist_ab = segment_distance(obj1.r[0], obj1.r[1], r_a[0], r_a[1], r_b[0], r_b[1])
    dist_bc = segment_distance(obj1.r[0], obj1.r[1], r_b[0], r_b[1], r_c[0], r_c[1])
    dist_cd = segment_distance(obj1.r[0], obj1.r[1], r_c[0], r_c[1], r_d[0], r_d[1])
    dist_da = segment_distance(obj1.r[0], obj1.r[1], r_d[0], r_d[1], r_a[0], r_a[1])

    if dist_ab <= obj1.scale or dist_bc <= obj1.scale or dist_cd <= obj1.scale or dist_da <= obj1.scale:
        return True
    else:
        return False


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
        if isinstance(obj, objects.Bullet):
            if dist[0] < 0 and abs(dist[0]) <= obj.scale:
                self.hit_dict['l'] = True
            if dist[0] > 0 and abs(dist[0]) <= self.block_size + obj.scale:
                self.hit_dict['r'] = True
            if dist[1] < 0 and abs(dist[1]) <= obj.scale:
                self.hit_dict['u'] = True
            if dist[1] > 0 and abs(dist[1]) <= self.block_size + obj.scale:
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


