import pygame


class Visual:

    # создание поля (описание его отображения на экране)
    def __init__(self):
        self.left = 10
        self.top = 10
        self.cell_size = 100

        self.height = 4
        self.width = 4
        self.board = [[0 for _ in range(self.height)] for _ in range(self.width)]

        # вывод на экран графического окна игры
        size_X = self.height * self.cell_size + self.left * 2
        size_Y = int((self.width + 0.7) * self.cell_size + self.top * 2)
        self.screen = pygame.display.set_mode((size_X, size_Y))

        # объявление цветовых констант
        self.clr_gainsboro = (220, 220, 220)        # цвет фона
        self.clr_lightseagreen = (32, 178, 170)     # цвет ячейки, фона при победе игрока и текста на кнопке "Try again"
        self.clr_lavenderblush = (255, 240, 245)    # цвет цифр, текста, кнопки для начала новой игры
        self.clr_white = (255, 255, 255)            # цвет границ между ячейками
        self.clr_red = (255, 0, 0)

        # объявление используемых шрифтов
        self.big_font = pygame.font.Font(None, self.cell_size)
        self.standard_font = pygame.font.Font(None, self.cell_size // 2)
        self.small_font = pygame.font.Font(None, self.cell_size // 4)

        # координаты, текст для отрисовки финального экрана и межстрочные интервалы
        self.pos_x = self.left + self.cell_size * 2
        self.pos_y = self.top + self.cell_size * 1
        self.text_soluble = ['Congratulations,', 'you won!', 'Your score: {}']
        self.text_insoluble = ['Oh, someone has confused all the chips,', 'and the task became intractable!',
                               'But you fought like a lion and brought', 'the game to the end. You won!',
                               'Your score: {}']
        self.interval_soluble = 0.5 * self.cell_size
        self.interval_insoluble = 0.3 * self.cell_size

    # отрисовка ячейки
    def draw_cell(self, clr, rind, cind):
        pygame.draw.rect(self.screen, clr, (self.left + cind * self.cell_size + self.cell_size / 10,
                                       self.top + rind * self.cell_size + self.cell_size / 10,
                                       self.cell_size * 0.8,
                                       self.cell_size * 0.8))

    # печать номера на ячейке (rind, cind -- координаты для печати)
    def print_number(self, num, rind, cind):
        text = self.big_font.render(num, 1, self.clr_lavenderblush)
        pos_x = self.left + cind * self.cell_size + self.cell_size // 2 - text.get_width() // 2
        pos_y = self.top + rind * self.cell_size + self.cell_size // 2 - text.get_height() // 2
        self.screen.blit(text, (pos_x, pos_y))

    # прорисовка границ
    def draw_borders(self, rind, cind):
        pygame.draw.rect(self.screen, self.clr_white, (self.left + cind * self.cell_size,  # прорисовка границ
                                                  self.top + rind * self.cell_size,
                                                  self.cell_size,
                                                  self.cell_size), 2)

    # изначальная отрисовка поля
    def st_render(self, arr, points):
        self.screen.fill(self.clr_gainsboro)
        for rind, row in enumerate(self.board):
            for cind, cell in enumerate(row):
                if arr[rind][cind] == '0':              # если ячейка имеет значение '0', оставим её пустой (серой)
                    self.draw_cell(self.clr_gainsboro, rind, cind)
                else:                                   # прорисовка ячеек
                    self.draw_cell(self.clr_lightseagreen, rind, cind)
                    self.print_number(arr[rind][cind], rind, cind)
                self.draw_borders(rind, cind)
        self.print_score(points)
        pygame.display.flip()                           # обновление содержимого всего экрана

    # отрисовка переставленных ячеек по их значениям и координатам
    def render(self, num, rind, cind, empty_y, empty_x, points):
        self.draw_cell(self.clr_lightseagreen, empty_y, empty_x)        # отрисовываем перемещенную ячейку
        self.print_number(num, empty_y, empty_x)
        self.draw_cell(self.clr_gainsboro, rind, cind)                  # отрисовываем новую пустую ячейку
        pygame.display.flip()                                           # обновление содержимого всего экрана

    # отображение текущего количества очков игрока
    def print_score(self, points):
        pygame.draw.rect(self.screen, self.clr_gainsboro,               # "закрашиваем" часть поля
                         (self.left + 0.7 * self.cell_size,
                          self.top + 4.1 * self.cell_size,
                          self.cell_size * 2.6,
                          self.cell_size * 0.6))
        pygame.draw.rect(self.screen, self.clr_white,                   # прорисовываем рамку # "закрашиваем" часть поля
                         (self.left + 0.7 * self.cell_size,
                          self.top + 4.1 * self.cell_size,
                          self.cell_size * 2.6,
                          self.cell_size * 0.6), 2)
        text = self.standard_font.render('Score: {}'.format(points), 1, self.clr_lightseagreen)
        pos_x = self.left + 2 * self.cell_size
        pos_y = self.top + 4.4 * self.cell_size
        place = text.get_rect(center=(pos_x, pos_y))
        self.screen.blit(text, place)
        pygame.display.flip()

    # отрисовка кнопки 'Try again :)'
    def draw_try_again_button(self):
        pygame.draw.rect(self.screen, self.clr_lavenderblush,           # отрисовываем поле для "кнопки"
                         (self.left + 0.7 * self.cell_size,
                          self.top + 3.1 * self.cell_size,
                          self.cell_size * 2.6,
                          self.cell_size * 0.8))
        text = self.standard_font.render('Try again :)', 1, self.clr_lightseagreen)
        pos_x = self.left + 2 * self.cell_size
        pos_y = self.top + 3.5 * self.cell_size
        place = text.get_rect(center=(pos_x, pos_y))
        self.screen.blit(text, place)

    # отрисовка поля в случае победы игрока, если комбинация была разрешима
    def win_screen_if_soluble(self, points):
        self.screen.fill(self.clr_lightseagreen)
        for i in range(len(self.text_soluble)):
            if i == len(self.text_soluble) - 1:
                string = self.standard_font.render(self.text_soluble[i].format(points), 1, self.clr_lavenderblush)
            else:
                string = self.standard_font.render(self.text_soluble[i], 1, self.clr_lavenderblush)
            place = string.get_rect(center=(self.pos_x, self.pos_y + self.interval_soluble * i))
            self.screen.blit(string, place)
        self.draw_try_again_button()
        pygame.display.flip()

    # отрисовка поля в случае победы игрока, если комбинация была неразрешима
    def win_screen_if_insoluble(self, points):
        self.screen.fill(self.clr_lightseagreen)
        self.screen.fill(self.clr_lightseagreen)
        for i in range(len(self.text_insoluble)):
            if i == len(self.text_insoluble) - 1:
                string = self.small_font.render(self.text_insoluble[i].format(points), 1, self.clr_lavenderblush)
            else:
                string = self.small_font.render(self.text_insoluble[i], 1, self.clr_lavenderblush)
            place = string.get_rect(center=(self.pos_x, self.pos_y + self.interval_insoluble * i))
            self.screen.blit(string, place)
        self.draw_try_again_button()
        pygame.display.flip()

    # проверяем, нажимает игрок на кнопку "Начать заново" или мимо неё
    def is_try_again_pressed(self, mouse_pos):
        pos_x = mouse_pos[0]
        pos_y = mouse_pos[1]
        if ((pos_x > self.left + 0.7 * self.cell_size) and (pos_x < self.left + 3.3 * self.cell_size)) \
           and ((pos_y > self.top + 3.1 * self.cell_size) and (pos_y < self.top + 3.9 * self.cell_size)):
            return True
        else:
            return False

    def get_cell(self, mouse_pos):
        cind = int((mouse_pos[0] - self.left)/self.cell_size)
        rind = int((mouse_pos[1] - self.top)/self.cell_size)
        if ((mouse_pos[0] > self.left) and (mouse_pos[0] < self.left + self.width * self.cell_size)) \
           and ((mouse_pos[1] > self.top) and (mouse_pos[1] < self.top + self.height * self.cell_size)):
            return rind, cind
        else:
            return -1, -1
