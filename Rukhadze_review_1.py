import pygame
import random

pygame.init()   # инициализация всех модулей библиотеки

pygame.display.set_caption("15 Puzzle")  # заголовок окна

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(height)] for _ in range(width)]
        self.list_of_endings = [['13', '15', '14', '0'], ['13', '15', '0', '14'],
                        ['13', '15', '0', '14'],['0', '13', '15', '14']]

        self.left = 10
        self.top = 10
        self.cell_size = 30

        # создание изначальной последовательности, в которой расположены ячейки
        numbers = list(map(str, range(16)))
        self.arr = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
        for i in range(16):
            a = random.choice(numbers)
            if a == '0':  # запоминаем изначальное положение пустой ячейки для дальнейшей проверки возможности сдвига
                self.empty_x = i % 4
                self.empty_y = i // 4
            numbers.remove(a)
            self.arr[i // 4][i % 4] = a

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # изначальная отрисовка поля
    def st_render(self):
        screen.fill((220, 220, 220))
        for rind, row in enumerate(self.board):
            for cind, cell in enumerate(row):
                font = pygame.font.Font(None, self.cell_size)  # подпись ячеек
                if self.arr[rind][cind] == '0':     # если ячейка имеет значение '0', оставим её пустой (серой)
                    pygame.draw.rect(screen, (220, 220, 220), (self.left + cind * self.cell_size + self.cell_size / 10,
                                                              self.top + rind * self.cell_size + self.cell_size / 10,
                                                              self.cell_size * 0.8,
                                                              self.cell_size * 0.8))

                else:                               # прорисовка ячеек
                    pygame.draw.rect(screen, (32, 178, 170), (self.left + cind * self.cell_size + self.cell_size / 10,
                                                              self.top + rind * self.cell_size + self.cell_size / 10,
                                                              self.cell_size * 0.8,
                                                              self.cell_size * 0.8))
                    text = font.render(self.arr[rind][cind], 1, (255, 240, 245))
                    text = font.render(self.arr[rind][cind], 1, (255, 240, 245))
                    pos_x = self.left + cind * self.cell_size + self.cell_size // 2 - text.get_width() // 2
                    pos_y = self.top + rind * self.cell_size + self.cell_size // 2 - text.get_height() // 2
                    screen.blit(text, (pos_x, pos_y))

                pygame.draw.rect(screen, (255, 255, 255), (self.left + cind * self.cell_size,  # прорисовка границ
                                                           self.top + rind * self.cell_size,
                                                           self.cell_size,
                                                           self.cell_size), 2)
        pygame.display.flip()  # обновление содержимого всего экрана

    # перерисовка игрового поля -- меняются местами 2 ячейки
    def render(self, rind, cind):   # нажатие на ячейку передвинет ячейку на свободное место, если этот ход возможен
            if (abs(self.empty_y - rind) + abs(self.empty_x - cind)) == 1:   # проверка условий передвижения
                pygame.draw.rect(screen, (32, 178, 170),    # отрисовываем перемещенную ячейку
                                (self.left + self.empty_x * self.cell_size + self.cell_size / 10,
                                 self.top + self.empty_y * self.cell_size + self.cell_size / 10,
                                 self.cell_size * 0.8,
                                 self.cell_size * 0.8))
                font = pygame.font.Font(None, self.cell_size)
                text = font.render(self.arr[rind][cind], 1, (255, 240, 245))
                pos_x = self.left + self.empty_x * self.cell_size + self.cell_size // 2 - text.get_width() // 2
                pos_y = self.top + self.empty_y * self.cell_size + self.cell_size // 2 - text.get_height() // 2
                screen.blit(text, (pos_x, pos_y))
                self.arr[self.empty_y][self.empty_x] = self.arr[rind][cind]  # обновляем значения пустой ячейки
                self.arr[rind][cind] = '0'
                self.empty_x = cind
                self.empty_y = rind
                pygame.draw.rect(screen, (220, 220, 220),  # отрисовываем новую пустую ячейку
                                (self.left + cind * self.cell_size + self.cell_size / 10,
                                 self.top + rind * self.cell_size + self.cell_size / 10,
                                 self.cell_size * 0.8,
                                 self.cell_size * 0.8))
            pygame.display.flip()  # обновление содержимого всего экрана

    # отрисовка поля в случае победы игрока, если комбинация была разрешима
    def print_win1(self):
        screen.fill((32, 178, 170))
        font = pygame.font.Font(None, self.cell_size // 2)
        text1 = font.render('Congratulations,', 1, (255, 240, 245))
        text2 = font.render('you won!', 1, (255, 240, 245))
        pos_x1 = self.left + self.cell_size * 2
        pos_y1 = self.top + self.cell_size * 1.5
        pos_x2 = self.left + self.cell_size * 2.65
        pos_y2 = self.top + self.cell_size * 2
        place1 = text1.get_rect(center=(pos_x1, pos_y1))
        place2 = text1.get_rect(center=(pos_x2, pos_y2))
        screen.blit(text1, place1)
        screen.blit(text2, place2)
        pygame.draw.rect(screen, (255, 240, 245),  # отрисовываем поле для "кнопки"
                         (self.left + 0.7 * self.cell_size,
                          self.top + 2.6 * self.cell_size,
                          self.cell_size * 2.6,
                          self.cell_size * 0.8))
        font = pygame.font.Font(None, self.cell_size // 2)
        text = font.render('Try again :)', 1, (32, 178, 170))
        pos_x = self.left + 1.1 * self.cell_size
        pos_y = self.top + 2.85 * self.cell_size
        screen.blit(text, (pos_x, pos_y))
        pygame.display.flip()

    # отрисовка поля в случае победы игрока, если комбинация была неразрешима
    def print_win2(self):
        screen.fill((32, 178, 170))
        font = pygame.font.Font(None, self.cell_size // 4)
        text1 = font.render('Oh, someone has  confused all the chips,', 1, (255, 240, 245))
        text2 = font.render('and the task became intractable!', 1, (255, 240, 245))
        text3 = font.render('But you fought like a lion and brought', 1, (255, 240, 245))
        text4 = font.render('the game to the end. You won!', 1, (255, 240, 245))
        pos_x1 = self.left + self.cell_size * 2
        pos_y1 = self.top + self.cell_size * 1.2
        pos_x2 = self.left + self.cell_size * 2.3
        pos_y2 = self.top + self.cell_size * 1.5
        pos_x3 = self.left + self.cell_size * 2.1
        pos_y3 = self.top + self.cell_size * 1.8
        pos_x4 = self.left + self.cell_size * 2.4
        pos_y4 = self.top + self.cell_size * 2.1
        place1 = text1.get_rect(center=(pos_x1, pos_y1))
        place2 = text1.get_rect(center=(pos_x2, pos_y2))
        place3 = text1.get_rect(center=(pos_x3, pos_y3))
        place4 = text1.get_rect(center=(pos_x4, pos_y4))
        screen.blit(text1, place1)
        screen.blit(text2, place2)
        screen.blit(text3, place3)
        screen.blit(text4, place4)
        pygame.draw.rect(screen, (255, 240, 245),  # отрисовываем поле для "кнопки"
                         (self.left + 0.7 * self.cell_size,
                          self.top + 2.6 * self.cell_size,
                          self.cell_size * 2.6,
                          self.cell_size * 0.8))
        font = pygame.font.Font(None, self.cell_size // 2)
        text = font.render('Try again :)', 1, (32, 178, 170))
        pos_x = self.left + 1.1 * self.cell_size
        pos_y = self.top + 2.85 * self.cell_size
        screen.blit(text, (pos_x, pos_y))
        pygame.display.flip()

    # функция, запускающаяся, если комбинация собрана
    def is_game_finished(self):
        t = self.arr.pop()
        if self.arr == [['1', '2', '3', '4'],
                        ['5', '6', '7', '8'],
                        ['9', '10', '11', '12']]:
            if t == ['13', '14', '15', '0']:
                pygame.time.delay(500)
                game_pole.print_win1()
                pygame.display.flip()  # обновление содержимого всего экрана
                return True
            elif t in self.list_of_endings:
                pygame.time.delay(500)
                game_pole.print_win2()
                return True
        self.arr.append(t)

    # функция, позволяющая начать новую игру
    def start_new_game(self):
        running = True
        while running:
            for event in pygame.event.get():  # перебор возможных действий игрока
                if event.type == pygame.QUIT:  # закрытие приложения
                    running = False
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие кнопкой мыши на ячейку
                    mouse_pos = event.pos
                    pos_x = mouse_pos[0]
                    pos_y = mouse_pos[1]
                    # проверяем, нажимает игрок на кнопку "Начать заново" или мимо неё
                    if ((pos_x > self.left + 0.7 * self.cell_size) and (pos_x < self.left + 3.3 * self.cell_size))\
                          and ((pos_y > self.top + 2.6 * self.cell_size) and (pos_y < self.top + 3.2 * self.cell_size)):
                        return True

    def get_cell(self, mouse_pos):
        cind, rind = int((mouse_pos[0] - self.left)/self.cell_size), int((mouse_pos[1] - self.top)/self.cell_size)
        if rind < len(self.board[0]) and cind < len(self.board):
            return rind, cind
        else:
            return 0, 0

class Game(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.is_started = False


if __name__ == '__main__':  # выполняется, если модуль был запущен, как самостоятельный
    outerrunning = True
    while outerrunning:
        x, y = 4, 4
        game_pole = Game(y, x)

        game_pole.set_view(10, 10, 100)

        size_X = game_pole.height * game_pole.cell_size + game_pole.top * 2
        size_Y = game_pole.width * game_pole.cell_size + game_pole.left * 2
        screen = pygame.display.set_mode((size_X, size_Y))  # вывод на экран графического окра игры

        mouse_btn_pressed = {1: False}

        mouse_pos = 0, 0
        game_pole.st_render()       # отрисовываем изначальную версию поля
        running = True
        while running:
            for event in pygame.event.get():    # перебор возможных действий игрока
                if event.type == pygame.QUIT:   # закрытие приложения
                    running = False
                    outerrunning = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие кнопкой мыши на ячейку
                    mouse_pos = event.pos
                    rind, cind = game_pole.get_cell(mouse_pos)
                    game_pole.render(rind, cind)
            if game_pole.is_game_finished():        # проверка на то, что игра завершена
                game_pole.is_game_finished()        # ячейки на финальном экране больше не отрисовываются
                if not game_pole.start_new_game():       # функция, позволяющая начать новую игру
                    running = False
                    outerrunning = False
                else:
                    running = False

    pygame.quit()  # гарантированное закрытие приложения
