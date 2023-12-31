
"""В этом файле описаны все игровые объекты кроме стен"""

import pygame

"""Класс танка, каждый объект задается своим начальным положением """


class Tank:
    def __init__(self, x, y, scale, type):
        self.type = type
        self.r = list([x, y])  # Координаты танка по осям х и у
        self.scale = scale  # Характерный размер танка
        self.v = [0, 0]  # Вектор скорости
        self.omega = 0.02  # Угловая скорость при поворотах
        self.ang = 0  # Изначально танк направлен вправо, угол в радианах и отсчитывается по часовой стрелке
        self.charges = 5  # Количество выстрелов
        # Хитбокс танка
        self.rect = pygame.Rect(self.r[0] - self.scale * 0.5, self.r[1] - self.scale * 0.5, self.scale, self.scale)
        # Параметры движения танка
        self.moving_front = False
        self.moving_back = False
        self.turning_left = False
        self.turning_right = False
        self.bonus = 'NONE'  # Информация о подобранном бонусе
        self.hp = 1  # Количество жизней, по умолчанию танк переживает 1 попадание


"""Класс пули, элементы задаются начальным положением и радиусом пули"""


class Bullet:
    def __init__(self, x, y, v, scale):
        self.r = list([x, y])  # Координаты танка по осям х и у
        self.scale = scale  # Радиус пули
        self.v = v  # Двумерный вектор со скоростями по осям
        self.life = 2  # Количество отскоков от стен прежде чем пуля исчезнет


"""Класс бонусов, элементы задаются положением (статичное) и типом бонуса"""


class Bonus:
    def __init__(self, x, y, var):
        self.r = [x, y]
        self.var = var  # Тип бонуса


"""Класс лазер, задается начальной и конечной точкой"""


class Laser:
    def __init__(self, r, end):
        self.r = r  # Начальная точка
        self.end = end  # Конечная точка
        self.life_time = 30  # Время, на протяжение которого лазер существует
        self.width = 10  # Толщина лазера
