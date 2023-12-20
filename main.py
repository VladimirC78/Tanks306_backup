import sys

from move_draw import *

"""Нужно будет загрузить картинки и звуки в папку проекта, image path  и ему подобные - переменные, в которые 
мы записываем путь на звуки и картинки(если загрузим в проект, то вместо полного пути можно будет использовать просто имя,
что удобнее) "is_hovered" отвечает за наведение, если конпка мыши находится где-то внутри кнопки, вместо обычной 
картинки кнопки отображается другая(например, более светлая) "handle_event" отвечает за воспроизведение звука при клике 
на кнопку
 """
screen_width = 800
screen_height = 600
pygame.init()
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
menu_background = pygame.image.load("menu_pics/settings.jpg")
settings_background = pygame.image.load("menu_pics/settings.jpg")


class Image_Button():
    def __init__(self, x, y, width, height, image_path, hover_image_path, sound_path=None):
        self.x = x  # координата х верхнего левого угла
        self.y = y  # координата у левого верхнего угла
        self.width = width  # размер по горизонтали
        self.height = height  # размер по вертикали
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = pygame.image.load(hover_image_path)
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
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


def main_menu(screen):
    start_button = Image_Button(screen_width / 2 - 252 / 2, 100, 252, 74, "menu_pics/start_button.png",
                                "menu_pics/hovered_start_button.png")
    quit_button = Image_Button(screen_width / 2 - 125, 250, 252, 74, "menu_pics/quit_button.png", "menu_pics/hovered_quit_button.png")
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
                running = False
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and settings_button.is_hovered:
                settings_menu(screen)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and quit_button.is_hovered:
                running = False
                pygame.quit()
                sys.exit()

        for button in buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)
        pygame.display.flip()


def settings_menu(screen):
    back_button = Image_Button(screen_width / 2 - 150 / 2, 500, 150, 74, "menu_pics/button_back.png", "menu_pics/hovered_button_back.png")
    buttons = [back_button]
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(settings_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and back_button.is_hovered:
                main_menu(screen)
        for button in buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)
        pygame.display.flip()


def main():
    screen = pygame.display.set_mode((1200, 800))
    walls_back = pygame.image.load('graphics/stena.jpg')
    tile = pygame.image.load('graphics/tile.jpg')
    breakable_wall1 = pygame.image.load('graphics/breakable_wall1.png')
    breakable_wall2 = pygame.image.load('graphics/breakable_wall2.png')
    breakable_wall3 = pygame.image.load('graphics/breakable_wall3.png')
    bullet_sign = pygame.image.load('graphics/bullet_sign.png')
    shield_sign = pygame.image.load('graphics/shield_sign.png')
    game_finished = False
    while not game_finished:
        level_finished = False
        screen.fill((255, 255, 255))
        walls, field, block_size = create_new_map()
        tanks = []
        bullets1 = []
        bullets2 = []
        bonuses = []
        flag = False
        timer1 = 0
        timer2 = 0
        bonus_timer = 0
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i][j] == 2:
                    if not flag:
                        tanks.append(objects.Tank(block_size * j, block_size * i, block_size, 1))
                        flag = True
                    else:
                        tanks.append(objects.Tank(block_size * j, block_size * i, block_size, 2))
        while not level_finished:
            pygame.display.update()
            screen.fill((255, 255, 255))
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

            for i in range(tanks[0].charges):
                screen.blit(bullet_sign, (i * 16 + 20, 20))

            for i in range(tanks[1].charges):
                screen.blit(bullet_sign, (1170 - i * 16, 20))

            if tanks[0].bonus == 'SHIELD':
                screen.blit(shield_sign, (37, 55))
            if tanks[1].bonus == 'SHIELD':
                screen.blit(shield_sign, (1122, 55))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and (tanks[1].bonus == 'NONE' or tanks[1].bonus == 'SHIELD'):
                        if tanks[1].charges > 0:
                            tanks[1].charges -= 1
                            timer2 = 0
                            r_center = [tanks[1].r[0] + 0.5 * tanks[1].scale * np.sin(-tanks[1].ang),
                                        tanks[1].r[1] - 0.5 * tanks[1].scale * np.cos(-tanks[1].ang)]
                            bullets2.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[1].ang), -4 * np.cos(tanks[1].ang)], 5))
                    elif event.key == pygame.K_SPACE:
                        if tanks[1].bonus == 'TRIPLESHOT':
                            r_center = [tanks[1].r[0] + 0.5 * tanks[1].scale * np.sin(-tanks[1].ang),
                                        tanks[1].r[1] - 0.5 * tanks[1].scale * np.cos(-tanks[1].ang)]
                            bullets2.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[1].ang), -4 * np.cos(tanks[1].ang)], 5))
                            bullets2.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[1].ang - 0.25), -4 * np.cos(tanks[1].ang - 0.25)], 5))
                            bullets2.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[1].ang + 0.25), -4 * np.cos(tanks[1].ang + 0.25)], 5))
                            tanks[1].bonus = 'NONE'

                        elif tanks[1].bonus == 'LASER':
                            print('LASER')
                            tanks[1].bonus = 'NONE'

                    if event.key == pygame.K_q and (tanks[0].bonus == 'NONE' or tanks[0].bonus == 'SHIELD'):
                        if tanks[0].charges > 0:
                            tanks[0].charges -= 1
                            timer1 = 0
                            r_center = [tanks[0].r[0] + 0.5 * tanks[0].scale * np.sin(-tanks[0].ang),
                                        tanks[0].r[1] - 0.5 * tanks[0].scale * np.cos(-tanks[0].ang)]
                            bullets1.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[0].ang), -4 * np.cos(tanks[0].ang)], 5))
                    elif event.key == pygame.K_q:
                        if tanks[0].bonus == 'TRIPLESHOT':
                            r_center = [tanks[0].r[0] + 0.5 * tanks[0].scale * np.sin(-tanks[0].ang),
                                        tanks[0].r[1] - 0.5 * tanks[0].scale * np.cos(-tanks[0].ang)]
                            bullets1.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[0].ang), -4 * np.cos(tanks[0].ang)], 5))
                            bullets1.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[0].ang - 0.25),
                                                            -4 * np.cos(tanks[0].ang - 0.25)], 5))
                            bullets1.append(objects.Bullet(r_center[0], r_center[1],
                                                           [-4 * np.sin(tanks[0].ang + 0.25),
                                                            -4 * np.cos(tanks[0].ang + 0.25)], 5))
                            tanks[0].bonus = 'NONE'

                        elif tanks[0].bonus == 'LASER':
                            print('LASER')
                            tanks[0].bonus = 'NONE'

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
                bullet_draw(screen, (255, 0, 0), b)
                bullet_move(b, walls)
                if b.life < 0:
                    bullets1.remove(b)
                if check_hit(tanks[1], b):
                    if tanks[1].bonus != 'SHIELD':
                        print("Победил игрок 1")
                        level_finished = True
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
                        print("Победил игрок 2")
                        level_finished = True
                    else:
                        tanks[0].bonus = 'NONE'
                        b.r[0] -= b.v[0] * 5
                        b.r[1] -= b.v[1] * 5
                        b.v[0] *= -1
                        b.v[1] *= -1

            for w in walls:
                if isinstance(w, BreakableWall):
                    if w.hp < 0:
                        field[int((w.r[1] - 0.5 * w.block_size) // w.block_size)][
                            int((w.r[0] - 0.5 * w.block_size) // w.block_size)] = 0
                        walls.remove(w)
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

            bonus_timer += 1
            if bonus_timer % 1500 == 0:
                chance = [0, 0]
                while field[chance[0]][chance[1]] == 1:
                    chance[0] = random.choice(range(len(field)))
                    chance[1] = random.choice(range(len(field[0])))
                var = random.choice(['SHIELD', 'TRIPLESHOT', 'LASER'])
                bonuses.append(objects.Bonus((chance[1] + 0.5) * block_size, (chance[0] + 0.5) * block_size, var))

            for bonus in bonuses:
                draw_bonus(screen, bonus)
                for t in tanks:
                    if bonus_pick(t, bonus):
                        t.bonus = bonus.var
                        bonuses.remove(bonus)


if __name__ == "__main__":
    main_menu(screen)
