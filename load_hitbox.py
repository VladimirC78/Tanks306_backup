"""В этом файле реализованы всевозможные взаимодействия между игровыми объектами, кроме того,
в нем вычисляются основные параметры карты"""

import random
import pygame

import Levels_encoded
import objects
import math

map_number = len(Levels_encoded.fields)

"""Функция, вычисляющая расстояние между 2 отрезками, позаимствована с qna.habr.com"""


def segm_dist(xa, ya, xb, yb, xc, yc, xd, yd):
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

    minimal = -1
    t = -2
    s = -2

    o = (xb - xa) * (-yd + yc) - (yb - ya) * (-xd + xc)
    o1 = (xb - xa) * (yc - ya) - (yb - ya) * (xc - xa)
    o2 = (-yd + yc) * (xc - xa) - (-xd + xc) * (yc - ya)

    if o != 0:
        t = o1 / o
        s = o2 / o

    if (t >= 0 and s >= 0) and (t <= 1 and s <= 1):
        minimal = 0  # Проверим пересекаются ли отрезки.
    else:
        # Найдём наименьшую высоту опущенную из конца одного отрезка на другой.
        dl1 = ras(xa, ya, xb, yb, xc, yc)
        minimal = dl1
        dl2 = ras(xa, ya, xb, yb, xd, yd)
        if (dl2 < minimal and dl2 != -1) or minimal == -1:
            minimal = dl2
        dl3 = ras(xc, yc, xd, yd, xa, ya)
        if (dl3 < minimal and dl3 != -1) or minimal == -1:
            minimal = dl3
        dl4 = ras(xc, yc, xd, yd, xb, yb)
        if (dl4 < minimal and dl4 != -1) or minimal == -1:
            minimal = dl4
        if minimal == -1:
            # В случае, если невозможно опустить высоту найдём минимальное расстояние между точками.
            dl1 = math.sqrt((xa - xc) * (xa - xc) + (ya - yc) * (ya - yc))
            minimal = dl1
            dl2 = math.sqrt((xb - xd) * (xb - xd) + (yb - yd) * (yb - yd))
            if dl2 < minimal:
                minimal = dl2
            dl3 = math.sqrt((xb - xc) * (xb - xc) + (yb - yc) * (yb - yc))
            if dl3 < minimal:
                minimal = dl3
        dl4 = math.sqrt((xa - xd) * (xa - xd) + (ya - yd) * (ya - yd))
        if dl4 < minimal:
            minimal = dl4
    return minimal


"""Функция, заполняющая массив стен карты, принимает на вход двумерный массив карты
и размер клетки (во всех картах 40 х 40)"""


def create_walls(field, block_size):
    walls = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                chance = random.choice(range(100))
                # С шансом 25% данная некраевая стена будет треснутой, то есть ее можно будет сломать выстрелами
                if chance <= 25 and i != 0 and j != 0 and i != len(field) - 1 and j != len(field[0]) - 1:
                    walls.append(BreakableWall(block_size, (j + 0.5) * block_size, (i + 0.5) * block_size))
                else:
                    walls.append(Wall(block_size, (j + 0.5) * block_size, (i + 0.5) * block_size))

    return walls


"""Функция, возвращающая все основные параметры карты - массив стен, двумерный массив поля и размер клетки"""


def create_new_map():
    map_choice = random.choice(range(map_number))
    field = Levels_encoded.fields[map_choice]
    scale_factor = 800 // len(field)
    block_size = scale_factor
    walls = create_walls(field, block_size)
    return walls, field, block_size


"""Функция, проверяющая попадание пули в танк, реализована при помощи pygame.rect.collidepoint.
Принимает на вход параметры танка и пули"""


def check_hit(obj1, obj2):
    x1 = obj1.rect.topleft[0] - obj2.scale
    y1 = obj1.rect.topleft[1] - obj2.scale
    # Увеличенный на радиус пули хитбокс танка
    hit_rect = pygame.Rect(x1, y1, obj1.scale + 2 * obj2.scale, obj1.scale + 2 * obj2.scale)
    if hit_rect.collidepoint(obj2.r):
        return True
    else:
        return False


"""Функция, проверяющая попадание лазера в танк, принимает параметры танка и лазера"""


def laser_hit(obj1, obj2):
    # Координаты вершин хитбокса танка
    r_a = obj1.rect.topleft
    r_b = obj1.rect.topright
    r_c = obj1.rect.bottomright
    r_d = obj1.rect.bottomleft
    # Расстояния между отрезками - сторонами хитбокса танка и лазером
    dist1 = segm_dist(r_a[0], r_a[1], r_b[0], r_b[1], obj2.r[0], obj2.r[1], obj2.end[0], obj2.end[1])
    dist2 = segm_dist(r_b[0], r_b[1], r_c[0], r_c[1], obj2.r[0], obj2.r[1], obj2.end[0], obj2.end[1])
    dist3 = segm_dist(r_c[0], r_c[1], r_d[0], r_d[1], obj2.r[0], obj2.r[1], obj2.end[0], obj2.end[1])
    dist4 = segm_dist(r_d[0], r_d[1], r_a[0], r_a[1], obj2.r[0], obj2.r[1], obj2.end[0], obj2.end[1])

    if dist1 == 0 or dist2 == 0 or dist3 == 0 or dist4 == 0:
        return True
    else:
        return False


"""Функция, проверяющая подбирание бонуса, принимает на вход данные о танке и бонусе"""


def bonus_pick(obj1, obj2):
    if obj1.rect.collidepoint(obj2.r):
        return True
    else:
        return False


"""Класс стен карты, элементы задаются размером клетки и положением центра"""


class Wall:
    def __init__(self, block_size, x, y):
        self.block_size = block_size
        self.r = list([x, y])
        self.hit_dict = {'u': False, 'd': False, 'r': False, 'l': False}
        self.rect = pygame.Rect(x - block_size * 0.5, y - block_size * 0.5, block_size, block_size)

    """Проверка на столкновение пули или танка со стеной, принимает на вход параметры объекта, возвращает словарь,
    в котором написано, с какой стороны от стены находится объект. Реализована на основе pygame.rect.collidepoint и
    pygame.rect.colliderect"""

    def wall_hit(self, obj):
        self.hit_dict = {'u': False, 'd': False, 'r': False, 'l': False}
        if isinstance(obj, objects.Bullet):
            # Для пули хитбокс стенки представляет собой 4 прямоугольника, находящиеся на сторонах стены
            # Толщина каждого из них равна радиусу пули
            top_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] - obj.scale, self.block_size, obj.scale)
            bot_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] + self.block_size, self.block_size,
                                   obj.scale)
            left_rect = pygame.Rect(self.rect.topleft[0] - obj.scale, self.rect.topleft[1], obj.scale, self.block_size)
            right_rect = pygame.Rect(self.rect.topleft[0] + self.block_size, self.rect.topleft[1], 2 * obj.scale,
                                     self.block_size)

            if left_rect.collidepoint(obj.r):
                self.hit_dict['l'] = True
            if right_rect.collidepoint(obj.r):
                self.hit_dict['r'] = True
            if top_rect.collidepoint(obj.r):
                self.hit_dict['u'] = True
            if bot_rect.collidepoint(obj.r):
                self.hit_dict['d'] = True
            if isinstance(self, BreakableWall):  # Если это треснутая стена, дополнительно отнимается ее здоровье
                if self.hit_dict['l'] or self.hit_dict['r'] or self.hit_dict['u'] or self.hit_dict['d']:
                    self.hp -= 1

        elif isinstance(obj, objects.Tank):
            # Для проверки столкновений танка со стеной хитбоксы стены - прямоугольники ее сторон
            wall_top_rect = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1] - 1, self.block_size, 1)
            wall_bot_rect = pygame.Rect(self.rect.bottomleft[0], self.rect.bottomleft[1], self.block_size, 1)
            wall_left_rect = pygame.Rect(self.rect.topleft[0] - 1, self.rect.topleft[1], 1, self.block_size)
            wall_right_rect = pygame.Rect(self.rect.topright[0], self.rect.topright[1], 1, self.block_size)
            # Хитбоксы танка при движении вперед аналогичен стенам, при движении назад хитбокс расширен,
            # так как иначе визуально картинка танка немного заходит за стену
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


"""Класс треснутой стены - наследник класса стен"""


class BreakableWall(Wall):
    def __init__(self, block_size, x, y):
        self.block_size = block_size
        self.r = list([x, y])
        self.hit_dict = {'u': False, 'd': False, 'r': False, 'l': False}
        self.rect = pygame.Rect(x - block_size * 0.5, y - block_size * 0.5, block_size, block_size)
        self.hp = 2
