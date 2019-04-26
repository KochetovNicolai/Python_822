import pygame
import random
import visualisation


class Board:

    # создание поля (данных о поле, а именно -- расположения ячеек на нем)
    def __init__(self):
        # выигрышная комбинация
        self.list_of_endings = [['13', '15', '14', '0'], ['13', '15', '0', '14'],
                                ['13', '15', '0', '14'], ['0', '13', '15', '14']]

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

        # количество очков игрока
        self.points = 500                           # изначальное количество очков
        self.standard_cost = 1                      # "стоимость" каждого хода
        self.extra_cost = 10                        # "стоимость" хода при перемещении ячейки на место пустой
        self.min_points = 0                         # минимально допустимое количество очков

    # функция, обновляющая расстановку ячеек (перестановка соседних ячеек стоит 1 очко, иначе -- 10)
    def swap_cells(self, rind, cind, myboard):
        if (abs(self.empty_y - rind) + abs(self.empty_x - cind)) == 1:      # проверка условий передвижения
            self.update_points(True)                                        # обновление количества очков
            myboard.render(self.arr[rind][cind], rind, cind, self.empty_y, self.empty_x, self.points)   # перестановка ячеек
            myboard.print_score(self.points)                                # вывод количества очков
            self.arr[self.empty_y][self.empty_x] = self.arr[rind][cind]     # обновление значений ячеек
            self.arr[rind][cind] = '0'
            self.empty_x = cind
            self.empty_y = rind
        elif (abs(self.empty_y - rind) + abs(self.empty_x - cind)) == 0:    # если игрок нажимает на пустую ячейку,
            pass                                                            # очки не снимаются
        elif (self.points - self.extra_cost) >= self.min_points:            # проверка, хватает ли у игрока очков
            self.update_points(False)                                       # далее аналогично предыдущему пункту
            myboard.render(self.arr[rind][cind], rind, cind, self.empty_y, self.empty_x, self.points)
            myboard.print_score(self.points)
            self.arr[self.empty_y][self.empty_x] = self.arr[rind][cind]
            self.arr[rind][cind] = '0'
            self.empty_x = cind
            self.empty_y = rind

    # функция, обновляющая количество очков игрока
    def update_points(self, flag):
        if flag:                                                                    # если кол-во очков минимально,
            self.points = max(self.points - self.standard_cost, self.min_points)    # игра продолжается
        else:                                               # нельзя переставлять не соседние ячейки,
            self.points = self.points - self.extra_cost     # если у игрока не хватает на это очков

    # функция, запускающаяся, если комбинация собрана
    def is_game_finished(self, myboard):
        t = self.arr.pop()
        if self.arr == [['1', '2', '3', '4'],
                        ['5', '6', '7', '8'],
                        ['9', '10', '11', '12']]:
            if t == ['13', '14', '15', '0']:
                pygame.time.delay(500)
                myboard.win_screen_if_soluble(self.points)
                pygame.display.flip()                       # обновление содержимого всего экрана
                return True
            elif (t in self.list_of_endings) and (self.points < self.extra_cost):   # запускается, если у игрока нет
                pygame.time.delay(500)                                              # очков на "бонусный" ход
                myboard.win_screen_if_insoluble(self.points)
                return True
        self.arr.append(t)

    # функция, позволяющая начать новую игру
    def start_new_game(self, myboard):
        running = True
        while running:
            for event in pygame.event.get():                # перебор возможных действий игрока
                if event.type == pygame.QUIT:               # закрытие приложения
                    running = False
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие кнопкой мыши на ячейку
                    mouse_pos = event.pos
                    if myboard.is_try_again_pressed(mouse_pos):
                        return True


class Game:

    def start(self):
        outerrunning = True
        while outerrunning:

            game_pole = Board()
            myboard = visualisation.Visual()                # создание визуального представления поля

            mouse_btn_pressed = {1: False}

            mouse_pos = 0, 0

            myboard.st_render(game_pole.arr, game_pole.points)  # отрисовываем изначальную версию поля

            running = True
            while running:
                for event in pygame.event.get():                # перебор возможных действий игрока
                    if event.type == pygame.QUIT:               # закрытие приложения
                        running = False
                        outerrunning = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:  # нажатие кнопкой мыши на ячейку
                        mouse_pos = event.pos
                        rind, cind = myboard.get_cell(mouse_pos)
                        if (rind + cind) != -2:                 # проверка, не нажал ли игрок за пределы игрового поля
                            game_pole.swap_cells(rind, cind, myboard)
                if game_pole.is_game_finished(myboard):         # проверка на то, что игра завершена
                    game_pole.is_game_finished(myboard)         # ячейки на финальном экране больше не отрисовываются
                    if not game_pole.start_new_game(myboard):   # функция, позволяющая начать новую игру
                        running = False
                        outerrunning = False
                    else:
                        running = False

        pygame.quit()  # гарантированное закрытие приложения
