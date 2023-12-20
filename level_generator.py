import matplotlib.pyplot as plt

field_size = [20, 30]


def equals(x, y):
    """Проверка равенства цветов"""
    if len(x) != len(x):
        return False
    for i in range(len(x)):
        if x[i] != y[i]:
            return False
    return True


def read_file(name):
    image = plt.imread('maps/' + name + '.bmp')
    if len(image) != field_size[0] or len(image[0]) != field_size[1]:
        print('Неверный размер поля')
    return image


def make_field(image):
    """Создает закодированное поле в виде двумерного массива"""
    field = [[0 for i in range(field_size[1])] for j in range(field_size[0])]
    for i in range(field_size[0]):
        for j in range(field_size[1]):
            if equals(image[i][j][:3], [0, 0, 0]):
                field[i][j] = 1
            elif equals(image[i][j][:3], [255, 0, 0]):
                field[i][j] = 2
    return field


name = input()
image = read_file(name)

print(make_field(image))

"""Инструкция: 
1) Создать картинку поля шириной 30 пикселей и высотой 20 пикселей, где стены будут черного цвета
2) Добавить ее в папку maps, сохранив в формате bmp
3) В окне ввода программы написать название файла без формата, например, просто test"""