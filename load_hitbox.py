import random

import numpy as np
import pygame

import Levels_encoded
import objects

map_number = len(Levels_encoded.fields)


def create_walls(field, block_size):
    # Создает стены
    walls = []
    breakable_walls = field
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                chance = random.choice(range(100))
                if chance <= 25 and i != 0 and j != 0 and i != len(field) - 1 and j != len(field[0]) - 1:
                    walls.append(BreakableWall(block_size, (j + 0.5) * block_size, (i + 0.5) * block_size))
                else:
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
            if isinstance(self, BreakableWall):
                if self.hit_dict['l'] or self.hit_dict['r'] or self.hit_dict['u'] or self.hit_dict['d']:
                    self.hp -= 1

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
