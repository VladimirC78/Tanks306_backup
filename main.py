import sys

from move_draw import *

screen_width = 800
screen_height = 600
pygame.init()
pygame.font.init()
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
menu_background = pygame.image.load("menu_pics/settings.jpg")
settings_background = pygame.image.load("menu_pics/settings.jpg")
vol = 1.0

pygame.mixer.music.load("music/music_path.mp3")
play_music = None

"""Класс кнопок меню"""


class Image_Button():
    def __init__(self, x, y, width, height, image_path, hover_image_path,
                 sound_path="music/knopka-klik-myagkii-blizkii-nizkii.wav"):
        self.x = x  # координата х верхнего левого угла
        self.y = y  # координата у левого верхнего угла
        self.width = width  # размер по горизонтали
        self.height = height  # размер по вертикали
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = pygame.image.load(hover_image_path)
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()


"""Функция, отображающая главное меню"""


def main_menu(screen, play_music, vol):
    if play_music == None:
        play_music = 1
    if play_music == 1:
        pygame.mixer.music.play(-1)

    start_button = Image_Button(screen_width / 2 - 252 / 2, 100, 252, 74, "menu_pics/start_button.png",
                                "menu_pics/hovered_start_button.png")
    quit_button = Image_Button(screen_width / 2 - 125, 250, 252, 74, "menu_pics/quit_button.png",
                               "menu_pics/hovered_quit_button.png")
    settings_button = Image_Button(screen_width / 2 - 252 / 2, 400, 252, 150, "menu_pics/settings_button.png",
                                   "menu_pics/hovered_settings_button.png")
    buttons = [start_button, settings_button, quit_button]
    running = True
    while running:

        screen.fill((0, 0, 0))
        screen.blit(menu_background, (-300, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start_button.is_hovered:
                running = False
                main()
            if event.type == pygame.QUIT:
                fade()
                running = False
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and settings_button.is_hovered:
                fade()
                settings_menu(screen, play_music, vol)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and quit_button.is_hovered:
                running = False
                pygame.quit()
                sys.exit()

        for button in buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)
        pygame.display.flip()


def fade():
    running = True
    fade_alpha = 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        fade_surface = pygame.Surface((1200, 800))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        fade_alpha += 5
        if fade_alpha >= 200:
            fade_alpha = 255
            running = False
        pygame.display.flip()


def settings_menu(screen, play_music, vol):
    normal_mute_button = "menu_pics/playing_mute_button.png"
    muted_mute_button = "menu_pics/muted_button.png"

    if play_music == 1 or play_music == 2:
        mute_button = normal_mute_button
        play_music = 2
    else:
        mute_button = muted_mute_button
    back_button = Image_Button(screen_width / 2 - 150 / 2, 500, 150, 74, "menu_pics/button_back.png",
                               "menu_pics/hovered_button_back.png")
    mute_button = Image_Button(screen_width / 2 - 150 / 2, 50, 150, 74, mute_button,
                               "menu_pics/hovered_mute_button.png")
    plus_button = Image_Button(screen_width / 2 - 120, 150, 100, 74, "menu_pics/plus_button.png",
                               "menu_pics/plus_button.png")
    minus_button = Image_Button(screen_width / 2, 181, 100, 12, "menu_pics/button_of_minus.png",
                                "menu_pics/button_of_minus.png")

    buttons = [back_button, mute_button, plus_button, minus_button]
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(settings_background, (0, 0))
        if play_music != 0 and vol > 0.01:
            text = 'Level of Volume ' + str(int(vol * 100)) + " %"
        else:
            text = "Level of Volume Mute"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_button.is_hovered:
                fade()
                main_menu(screen, play_music, vol)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mute_button.is_hovered:
                if play_music:
                    pygame.mixer.music.pause()
                    play_music = 0
                    text = "Mute"
                else:
                    pygame.mixer.music.unpause()
                    play_music = 2

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and plus_button.is_hovered:
                vol += 0.1

                pygame.mixer.music.set_volume(vol)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and minus_button.is_hovered:
                vol -= 0.1
                pygame.mixer.music.set_volume(vol)

        text_surface = my_font.render(text, False, (255, 255, 255))
        screen.blit(text_surface, (460, 0))
        for button in buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        pygame.display.flip()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font((pygame.font.match_font('ink free')), size)
    text_surface = font.render(text, True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


""""""
"""Функция, отображающая переход между уровнями при поражении одного из игроков"""


def perexod(slova, slova2):
    dead = pygame.image.load("menu_pics/dead.jpg")
    screen.blit(dead, (180, 80))
    draw_text(screen, "GAME OVER", 120, 1200 / 2, 800 / 4)
    draw_text(screen, slova, 50, 1200 / 2, 800 / 2)
    draw_text(screen, slova2, 50, 1200 / 2, 800 * 5 / 8)
    draw_text(screen, "Press F key to begin", 30, 1200 / 2, 800 * 3 / 4)
    pygame.display.flip()
    # for event in pygame.event.get():
    #     if event.key == pygame.K_f:


def main():
    # Параметры игрового окна
    width = 1200
    height = 800
    screen = pygame.display.set_mode((width, height))
    # Загрузка картинок из папки graphics
    walls_back = pygame.image.load('graphics/stena.jpg')
    tile = pygame.image.load('graphics/tile.jpg')
    breakable_wall1 = pygame.image.load('graphics/breakable_wall1.png')
    breakable_wall2 = pygame.image.load('graphics/breakable_wall2.png')
    breakable_wall3 = pygame.image.load('graphics/breakable_wall3.png')
    bullet_sign = pygame.image.load('graphics/bullet_sign.png')
    shield_sign = pygame.image.load('graphics/shield_sign.png')
    bonus_shield = pygame.image.load('graphics/bonus_shield.png')
    bonus_triple = pygame.image.load('graphics/bonus_triple.png')
    bonus_laser = pygame.image.load('graphics/bonus_laser.png')
    sound_of_bullet = pygame.mixer.Sound("music/vyistrel-pistoleta-36125.wav")
    sound_of_laser = pygame.mixer.Sound("music/orujie-lazer.wav")
    imgs = [bonus_shield, bonus_triple, bonus_laser]

    game_finished = False
    level_finished = False
    p1 = 0
    p2 = 0
    v_bullet = 4

    while not game_finished:
        # Внешний игровой цикл, с каждой итерацией создает новый уровень
        if level_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        level_finished = False
            perexod(slova, slova2)
        else:
            screen.fill((255, 255, 255))
            walls, field, block_size = create_new_map()  # Основные параметры карты
            # Массивы объектов
            tanks = []
            bullets1 = []
            bullets2 = []
            bonuses = []
            lasers2 = []
            lasers1 = []

            dead_timer1 = 0  # Таймеры, запускающиеся после поражения одного из игроков
            dead_timer2 = 0

            flag = False

            timer1 = 0  # Таймеры перезарядки танков
            timer2 = 0
            bonus_timer = 0  # Таймер появления бонусов
            # Спавн танков в определенных точках карты
            for i in range(len(field)):
                for j in range(len(field[i])):
                    if field[i][j] == 2:
                        if not flag:
                            tanks.append(objects.Tank(block_size * j, block_size * i, block_size, 1))
                            flag = True
                        else:
                            tanks.append(objects.Tank(block_size * j, block_size * i, block_size, 2))
            while not level_finished:
                # Игровой цикл уровня
                pygame.display.update()
                screen.fill((255, 255, 255))
                # Отрисовка карты
                for i in range(len(field)):
                    for j in range(len(field[i])):
                        if field[i][j] == 0 or field[i][j] == 2:
                            screen.blit(tile, (block_size * j, block_size * i))
                for w in walls:
                    if isinstance(w, BreakableWall):
                        if w.hp == 2:
                            screen.blit(breakable_wall1, (w.r[0] - 0.5 * w.block_size, w.r[1] - 0.5 * w.block_size))
                        elif w.hp == 1:
                            screen.blit(breakable_wall2, (w.r[0] - 0.5 * w.block_size, w.r[1] - 0.5 * w.block_size))
                        elif w.hp == 0:
                            screen.blit(breakable_wall3, (w.r[0] - 0.5 * w.block_size, w.r[1] - 0.5 * w.block_size))
                    else:
                        screen.blit(walls_back, (w.r[0] - 0.5 * w.block_size, w.r[1] - 0.5 * w.block_size))

                # Элементы интерфейса - количество выстрелов и наличие щита у игрока
                for i in range(tanks[0].charges):
                    screen.blit(bullet_sign, (i * 16 + 20, 20))

                for i in range(tanks[1].charges):
                    screen.blit(bullet_sign, (1170 - i * 16, 20))

                if tanks[0].bonus == 'SHIELD':
                    screen.blit(shield_sign, (37, 55))
                if tanks[1].bonus == 'SHIELD':
                    screen.blit(shield_sign, (1122, 55))

                # Мониторинг событий
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        # Вычисление положения дула танка в момент выстрела
                        r_center1 = [tanks[1].r[0] + 0.5 * tanks[1].scale * np.sin(-tanks[1].ang),
                                     tanks[1].r[1] - 0.5 * tanks[1].scale * np.cos(-tanks[1].ang)]
                        r_center0 = [tanks[0].r[0] + 0.5 * tanks[0].scale * np.sin(-tanks[0].ang),
                                     tanks[0].r[1] - 0.5 * tanks[0].scale * np.cos(-tanks[0].ang)]
                        if event.key == pygame.K_SPACE and (tanks[1].bonus == 'NONE' or tanks[1].bonus == 'SHIELD'):
                            # Обычный выстрел - если не подобраны бонусы вроде лазера или тройного выстрела
                            if tanks[1].charges > 0:
                                sound_of_bullet.play()
                                tanks[1].charges -= 1
                                timer2 = 0
                                bullets2.append(objects.Bullet(r_center1[0], r_center1[1],
                                                               [-v_bullet * np.sin(tanks[1].ang),
                                                                -v_bullet * np.cos(tanks[1].ang)],
                                                               5))
                        elif event.key == pygame.K_SPACE:
                            if tanks[1].bonus == 'TRIPLESHOT':
                                sound_of_bullet.play()
                                # Тройной выстрел - создаются 2 дополнительные пули под одинаковым углом
                                # к основному направлению
                                bullets2.append(objects.Bullet(r_center1[0], r_center1[1],
                                                               [-v_bullet * np.sin(tanks[1].ang),
                                                                -v_bullet * np.cos(tanks[1].ang)],
                                                               5))
                                bullets2.append(objects.Bullet(r_center1[0], r_center1[1],
                                                               [-v_bullet * np.sin(tanks[1].ang - 0.25),
                                                                -v_bullet * np.cos(tanks[1].ang - 0.25)], 5))
                                bullets2.append(objects.Bullet(r_center1[0], r_center1[1],
                                                               [-v_bullet * np.sin(tanks[1].ang + 0.25),
                                                                -v_bullet * np.cos(tanks[1].ang + 0.25)], 5))
                                tanks[1].bonus = 'NONE'

                            elif tanks[1].bonus == 'LASER':
                                sound_of_laser.play()
                                # Расчет положения конечной точки отрезка в зависимости от угла поворота и координат
                                # танка
                                if np.sin(-tanks[1].ang) > 0:
                                    y_edge = r_center1[1] - (width - r_center1[0]) / np.tan(-tanks[1].ang)
                                elif np.sin(-tanks[1].ang) == 0 and np.cos(-tanks[1].ang) == -1:
                                    y_edge = height
                                elif np.sin(-tanks[1].ang) == 0 and np.cos(-tanks[1].ang) == 1:
                                    y_edge = 0
                                else:
                                    y_edge = r_center1[1] + r_center1[0] / np.tan(-tanks[1].ang)

                                if y_edge >= height:
                                    end = [r_center1[0] + (r_center1[1] - height) * np.tan(-tanks[1].ang), height]
                                elif y_edge <= 0:
                                    end = [r_center1[0] + r_center1[1] * np.tan(-tanks[1].ang), 0]
                                else:
                                    if np.sin(-tanks[1].ang) < 0:
                                        end = [0, y_edge]
                                    else:
                                        end = [width, y_edge]
                                lasers2.append(objects.Laser(r_center1, end))
                                tanks[1].bonus = 'NONE'

                        # Аналогично для другого танка

                        if event.key == pygame.K_q and (tanks[0].bonus == 'NONE' or tanks[0].bonus == 'SHIELD'):
                            if tanks[0].charges > 0:
                                sound_of_bullet.play()
                                tanks[0].charges -= 1
                                timer1 = 0
                                bullets1.append(objects.Bullet(r_center0[0], r_center0[1],
                                                               [-v_bullet * np.sin(tanks[0].ang),
                                                                -v_bullet * np.cos(tanks[0].ang)],
                                                               5))
                        elif event.key == pygame.K_q:
                            if tanks[0].bonus == 'TRIPLESHOT':
                                sound_of_bullet.play()
                                bullets1.append(objects.Bullet(r_center0[0], r_center0[1],
                                                               [-v_bullet * np.sin(tanks[0].ang),
                                                                -v_bullet * np.cos(tanks[0].ang)],
                                                               5))
                                bullets1.append(objects.Bullet(r_center0[0], r_center0[1],
                                                               [-v_bullet * np.sin(tanks[0].ang - 0.25),
                                                                -v_bullet * np.cos(tanks[0].ang - 0.25)], 5))
                                bullets1.append(objects.Bullet(r_center0[0], r_center0[1],
                                                               [-v_bullet * np.sin(tanks[0].ang + 0.25),
                                                                -v_bullet * np.cos(tanks[0].ang + 0.25)], 5))
                                tanks[0].bonus = 'NONE'

                            elif tanks[0].bonus == 'LASER':
                                sound_of_laser.play()
                                if np.sin(-tanks[0].ang) > 0:
                                    y_edge = r_center0[1] - (width - r_center0[0]) / np.tan(-tanks[0].ang)
                                elif np.sin(-tanks[0].ang) == 0 and np.cos(-tanks[0].ang) == -1:
                                    y_edge = height
                                elif np.sin(-tanks[0].ang) == 0 and np.cos(-tanks[0].ang) == 1:
                                    y_edge = 0
                                else:
                                    y_edge = r_center0[1] + r_center0[0] / np.tan(-tanks[0].ang)

                                if y_edge >= height:
                                    end = [r_center0[0] + (r_center0[1] - height) * np.tan(-tanks[0].ang), height]
                                elif y_edge <= 0:
                                    end = [r_center0[0] + r_center0[1] * np.tan(-tanks[0].ang), 0]
                                else:
                                    if np.sin(-tanks[0].ang) < 0:
                                        end = [0, y_edge]
                                    else:
                                        end = [width, y_edge]
                                lasers1.append(objects.Laser(r_center0, end))
                                tanks[0].bonus = 'NONE'

                        # Изменение статуса танка при нажатии на клавиши движения

                        if event.key == pygame.K_w:
                            tanks[0].moving_front = True
                        if event.key == pygame.K_s:
                            tanks[0].moving_back = True
                        if event.key == pygame.K_a:
                            tanks[0].turning_left = True
                        if event.key == pygame.K_d:
                            tanks[0].turning_right = True
                        if event.key == pygame.K_UP:
                            tanks[1].moving_front = True
                        if event.key == pygame.K_DOWN:
                            tanks[1].moving_back = True
                        if event.key == pygame.K_LEFT:
                            tanks[1].turning_left = True
                        if event.key == pygame.K_RIGHT:
                            tanks[1].turning_right = True

                    # Остановка танка при отпускании клавиш движения

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w or event.key == pygame.K_s:
                            tanks[0].moving_front = False
                            tanks[0].moving_back = False
                        if event.key == pygame.K_a or event.key == pygame.K_d:
                            tanks[0].turning_right = False
                            tanks[0].turning_left = False
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            tanks[1].moving_front = False
                            tanks[1].moving_back = False
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            tanks[1].turning_right = False
                            tanks[1].turning_left = False

                for t in tanks:
                    # Передвижение танков в зависимости от взаимного расположения со стенами
                    # Используется функция move_tank из move_draw, vx и vy меняются в зависимости от наличия
                    # стен поблизости
                    t.rect = draw_tank(t, screen)
                    vx = 1
                    vy = 1
                    for w in walls:
                        if w.wall_hit(t)['l']:
                            if t.moving_front:
                                if np.sin(t.ang) < 0:
                                    vx = 0
                                    if t.r[0] >= w.r[0] - (w.block_size + t.scale) * 0.4:
                                        t.r[0] = w.r[0] - (w.block_size + t.scale) * 0.4
                            if t.moving_back:
                                if np.sin(t.ang) > 0:
                                    vx = 0
                                    if t.r[0] >= w.r[0] - (w.block_size + t.scale) * 0.4:
                                        t.r[0] = w.r[0] - (w.block_size + t.scale) * 0.4
                        if w.wall_hit(t)['r']:
                            if t.moving_front:
                                if np.sin(t.ang) > 0:
                                    vx = 0
                                    if t.r[0] <= w.r[0] + (w.block_size + t.scale) * 0.4:
                                        t.r[0] = w.r[0] + (w.block_size + t.scale) * 0.4
                            if t.moving_back:
                                if np.sin(t.ang) < 0:
                                    vx = 0
                                    if t.r[0] <= w.r[0] + (w.block_size + t.scale) * 0.4:
                                        t.r[0] = w.r[0] + (w.block_size + t.scale) * 0.4
                        if w.wall_hit(t)['u']:
                            if t.moving_front:
                                if np.cos(t.ang) < 0:
                                    vy = 0
                                    if t.r[1] >= w.r[1] - (w.block_size + t.scale) * 0.4:
                                        t.r[1] = w.r[1] - (w.block_size + t.scale) * 0.4
                            if t.moving_back:
                                if np.cos(t.ang) > 0:
                                    vy = 0
                                    if t.r[1] >= w.r[1] - (w.block_size + t.scale) * 0.4:
                                        t.r[1] = w.r[1] - (w.block_size + t.scale) * 0.4
                        if w.wall_hit(t)['d']:
                            if t.moving_front:
                                if np.cos(t.ang) > 0:
                                    vy = 0
                                    if t.r[1] <= w.r[1] + (w.block_size + t.scale) * 0.4:
                                        t.r[1] = w.r[1] + (w.block_size + t.scale) * 0.4
                            if t.moving_back:
                                if np.cos(t.ang) < 0:
                                    vy = 0
                                    if t.r[1] <= w.r[1] + (w.block_size + t.scale) * 0.4:
                                        t.r[1] = w.r[1] + (w.block_size + t.scale) * 0.4
                    move_tank(t, vx, vy)

                for b in bullets1:
                    # Передвижение, отрисовка и проверка пули на попадание
                    bullet_draw(screen, (255, 0, 0), b)
                    bullet_move(b, walls)
                    if b.life < 0:
                        bullets1.remove(b)
                    if check_hit(tanks[1], b):
                        if tanks[1].bonus != 'SHIELD':
                            tanks[1].hp -= 1

                            bullets1.remove(b)
                        else:
                            tanks[1].bonus = 'NONE'
                            b.r[0] -= b.v[0] * 5
                            b.r[1] -= b.v[1] * 5
                            b.v[0] *= -1
                            b.v[1] *= -1

                for b in bullets2:
                    bullet_draw(screen, (0, 128, 0), b)
                    bullet_move(b, walls)
                    if b.life < 0:
                        bullets2.remove(b)
                    if check_hit(tanks[0], b):
                        if tanks[0].bonus != 'SHIELD':
                            tanks[0].hp -= 1
                            bullets2.remove(b)
                        else:
                            tanks[0].bonus = 'NONE'
                            b.r[0] -= b.v[0] * 5
                            b.r[1] -= b.v[1] * 5
                            b.v[0] *= -1
                            b.v[1] *= -1

                # Завершение уровня после поражения одного из игроков
                if tanks[0].hp <= 0:
                    dead_timer1 += 1
                    if dead_timer1 >= 30:
                        level_finished = True
                        slova = ('Player 2 win')
                        p2 += 1
                        slova2 = f'Score P1: {p1}, P2 {p2}'
                elif tanks[1].hp <= 0:
                    dead_timer2 += 1
                    if dead_timer2 >= 30:
                        level_finished = True
                        slova = ('Player 1 win')
                        p1 += 1
                        slova2 = f'Score P1:{p1}, P2:{p2}'

                # Удаление разбитой стены
                for w in walls:
                    if isinstance(w, BreakableWall):
                        if w.hp < 0:
                            field[int((w.r[1] - 0.5 * w.block_size) // w.block_size)][
                                int((w.r[0] - 0.5 * w.block_size) // w.block_size)] = 0
                            walls.remove(w)

                # Перезарядка со временем
                if tanks[0].charges < 5:
                    timer1 += 1
                if tanks[1].charges < 5:
                    timer2 += 1

                if timer1 % 200 == 0:
                    if tanks[0].charges < 5:
                        tanks[0].charges += 1
                if timer2 % 200 == 0:
                    if tanks[1].charges < 5:
                        tanks[1].charges += 1

                # Появление бонуса через равные интервалы времени
                bonus_timer += 1
                if bonus_timer % 1000 == 0 and len(bonuses) <= 5:
                    chance = [0, 0]
                    while field[chance[0]][chance[1]] == 1:
                        chance[0] = random.choice(range(len(field)))
                        chance[1] = random.choice(range(len(field[0])))
                    var = random.choice(['SHIELD', 'TRIPLESHOT', 'LASER'])
                    bonuses.append(objects.Bonus((chance[1] + 0.5) * block_size, (chance[0] + 0.5) * block_size, var))

                # Отрисовка и обработка подбирания бонуса
                for bonus in bonuses:
                    draw_bonus(screen, bonus, imgs)
                    for t in tanks:
                        if bonus_pick(t, bonus):
                            t.bonus = bonus.var
                            bonuses.remove(bonus)

                # Отрисовка и проверка попадания лазера
                for laser in lasers2:
                    draw_laser(screen, laser, (0, 0, 255))
                    laser.life_time -= 1
                    if laser.life_time <= 0:
                        lasers2.remove(laser)
                    if laser_hit(tanks[0], laser):
                        tanks[0].hp -= 1

                for laser in lasers1:
                    draw_laser(screen, laser, (255, 0, 0))
                    laser.life_time -= 1
                    if laser.life_time <= 0:
                        lasers1.remove(laser)
                    if laser_hit(tanks[1], laser):
                        tanks[1].hp -= 1


if __name__ == "__main__":
    main_menu(screen, play_music, vol)
