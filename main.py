import pygame
import sys
from load_hitbox import *
import objects
from move_draw import tank_move, bullet_move

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
menu_background = pygame.image.load("settings.jpg")
settings_background = pygame.image.load("settings.jpg")


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
    start_button = Image_Button(screen_width / 2 - 252 / 2, 100, 252, 74, "start_button.png",
                                "hovered_start_button.png")
    quit_button = Image_Button(screen_width / 2 - 125, 250, 252, 74, "quit_button.png", "hovered_quit_button.png")
    settings_button = Image_Button(screen_width / 2 - 252 / 2, 400, 252, 150, "settings_button.png",
                                   "hovered_settings_button.png")
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
    back_button = Image_Button(screen_width / 2 - 150 / 2, 500, 150, 74, "button_back.png", "hovered_button_back.png")
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
    game_finished = False
    level_finished = False
    while not game_finished:

        screen.fill((255, 255, 255))
        walls, field, block_size = create_new_map()
        tanks = []
        bullets1 = []
        bullets2 = []
        flag = False
        for i in range(len(field)):
            for j in range(len(field[i])):
                if field[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (block_size * j, block_size * i, block_size, block_size))
                if field[i][j] == 2:
                    if not flag:
                        tanks.append(objects.Tank(block_size * j, block_size * i, 0.01, block_size, 1))
                        flag = True
                    else:
                        tanks.append(objects.Tank(block_size * j, block_size * i, 0.01, block_size, 2))
        while not level_finished:
            pygame.display.update()
            screen.fill((255, 255, 255))
            for i in range(len(field)):
                for j in range(len(field[i])):
                    if field[i][j] == 1:
                        pygame.draw.rect(screen, (0, 0, 0), (block_size * j, block_size * i, block_size, block_size))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    r_center = [tanks[1].r[0] + 0.65 * tanks[1].scale * np.sin(-tanks[1].ang),
                                tanks[1].r[1] - 0.65 * tanks[1].scale * np.cos(-tanks[1].ang)]
                    bullets2.append(
                        objects.Bullet(r_center[0], r_center[1], [-2 * np.sin(tanks[1].ang), -2 * np.cos(tanks[1].ang)],
                                       5))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    r_center = [tanks[0].r[0] + 0.65 * tanks[0].scale * np.sin(-tanks[0].ang),
                                tanks[0].r[1] - 0.65 * tanks[0].scale * np.cos(-tanks[0].ang)]
                    bullets1.append(
                        objects.Bullet(r_center[0], r_center[1], [-2 * np.sin(tanks[0].ang), -2 * np.cos(tanks[0].ang)],
                                       5))
            for t in tanks:
                t.rect = t.draw(screen)
                tank_move(t, walls)

            for b in bullets1:
                b.draw(screen)
                bullet_move(b, walls)
                if check_hit(tanks[1], b):
                    print("Есть пробитие")

            for b in bullets2:
                b.draw(screen)
                bullet_move(b, walls)
                if check_hit(tanks[0], b):
                    print("Есть пробитие")


if __name__ == "__main__":
    main_menu(screen)
