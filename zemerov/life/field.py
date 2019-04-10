import pygame
import button
import colours


class Field:
    """Основной класс, который будет управлять игровым полем"""
    height = 12
    width = 12
    margin = 2
    menu_height = 30

    FONT = 'arial'
    FONT_SIZE = 40

    def __init__(self, number=40):
        self.number = number
        self.score = 0  # Максимальное количество клеток за игру
        # Заполняем игровое поле нулями
        self.grid = [[0 for x in range(number)] for y in range(number)]

        # Задаём квадратное поле
        self.field_size = (
            number * Field.height + (number + 1) * Field.margin,
            number * Field.height + (number + 1) * Field.margin + Field.menu_height,
        )

        self.pure_height = number * Field.height + (number + 1) * Field.margin
        self.pure_width = number * Field.height + (number + 1) * Field.margin

        # Счётчик живых клеток
        self.live_cells = 0
        self.is_dead = False

        self.previous = []

    def draw(self, surface):
        """Отрисовывает на surface игровое поле на текущий момент"""

        for row in range(self.number):
            for column in range(self.number):
                color = colours.WHITE
                if self.grid[row][column] == 1:
                    color = colours.BLUE
                pygame.draw.rect(surface,
                                 color,
                                 [(Field.margin + Field.width) * column + Field.margin,
                                  (Field.margin + Field.height) * row + Field.margin,
                                  Field.width,
                                  Field.height])

    def click(self, place):
        """Изменение состояния клетки пользователем"""

        column = min(place[0] // (Field.width + Field.margin), self.number - 1)
        row = min(place[1] // (Field.height + Field.margin), self.number - 1)

        if self.grid[row][column] == 1:
            self.grid[row][column] = 0
            self.live_cells -= 1
        else:
            self.grid[row][column] = 1
            self.live_cells += 1

    def evolution_step(self):
        """Обновляет состояние живых и мертвых клеток"""

        tmp = [[0 for x in range(self.number)] for y in range(self.number)]
        tmp_num = 0

        for i in range(self.number):
            for j in range(self.number):
                n_neigh = self.__count_neighbours__(i, j)
                if self.grid[i][j] == 0 and n_neigh == 3:
                    tmp[i][j] = 1
                    tmp_num += 1
                elif self.grid[i][j] == 1 and (n_neigh == 2 or n_neigh == 3):
                    tmp[i][j] = 1
                    tmp_num += 1
                else:
                    tmp[i][j] = 0

        if tmp_num == 0:
            self.is_dead = True
        else:
            self.live_cells = tmp_num

        self.score = max(self.score, tmp_num)

        if len(self.previous) > 10:
            self.previous.pop(0)

        self.previous.append(self.grid)  # Добавляем текующую конфигурацию в previous

        if tmp in self.previous:
            self.is_dead = True

        self.grid = tmp

    def __count_neighbours__(self, row, column):
        """Подсчёт количества соседей"""

        ans = 0
        # Обработать крайние клетки
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == j == 0):
                    if row == 0 and i == -1:
                        continue
                    elif row == self.number - 1 and i == 1:
                        continue
                    elif column == 0 and j == -1:
                        continue
                    elif column == self.number - 1 and j == 1:
                        continue

                    ans += self.grid[row + i][column + j]

        return ans

    def refresh(self):
        """В случае restart происходит обновление игрового поля"""

        self.grid = [[0 for x in range(self.number)] for y in range(self.number)]

        self.score = 0
        self.live_cells = 0
        self.is_dead = False

    def game_over(self, surface):
        game_over_text = button.Button(
            'GAME OVER',
            Field.FONT,
            Field.FONT_SIZE,
            160,
            150,
            colours.WHITE,
            colours.GAMEOVER
        )

        score_text = button.Button(
            'MAX SCORE {}'.format(self.score),
            Field.FONT,
            Field.FONT_SIZE,
            140,
            190,
            colours.WHITE,
            colours.GAMEOVER
        )
        window = pygame.Surface((self.pure_width, self.pure_height))
        window.set_alpha(2)
        window.fill(colours.GAMEOVER)
        surface.blit(window, (0, 0))
        game_over_text.draw(surface, is_rect=False)
        score_text.draw(surface, is_rect=False)
