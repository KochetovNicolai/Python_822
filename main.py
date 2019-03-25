#!/usr/bin/env python

from __future__ import print_function
import random
from queue import Queue
import tkinter as tk
from PIL import Image, ImageTk
import sys

# Окно вывода изображения на экран
class ExampleApp(tk.Tk):

    # Отступ налево
    def _draw_image_left(self, event):
        if self.counter_x > 0: self.counter_x -= 1
        self._draw_image()

    # Отступ вправо
    def _draw_image_right(self, event):
        self.counter_x += 1
        self._draw_image()

    # Отступ наверх
    def _draw_image_up(self, event):
        if self.counter_y > 0: self.counter_y -= 1
        self._draw_image()

    # Отступ вниз
    def _draw_image_down(self, event):
        self.counter_y += 1
        self._draw_image()

    # Инициализация окна вывода
    def __init__(self, master, array):
        # Указание наименований текстур, импортируемых в вывод *позиция имеет значение!!!*
        self.names = ['Water_deep.png', 'Plains.png', 'Forests.png', 'Mountains.png', 'Snowy_mountains.png', 'Water_not_deep.png']

        self.counter_x = self.counter_y = 0

        self.array = array
        self.tk_im = []
        self.items = []

        # Указание размеров canvas
        self.canvas = tk.Canvas(master, width=512, height=512, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Привязка нажатий на кнопки к соответствующим событиям
        master.bind("<Up>", self._draw_image_up)
        master.bind("<Down>", self._draw_image_down)
        master.bind("<Left>", self._draw_image_left)
        master.bind("<Right>", self._draw_image_right)

        # Создание массива текстур, для ускорения работы вывода изображений
        for name in self.names:
            self.im = Image.open(name)
            self.tk_im.append(ImageTk.PhotoImage(self.im))

        # Первичная отрисовка
        self._draw_image()

    # Вывод картинок на канвас
    def _draw_image(self):

        # Очистка старого вывода
        self.items.clear()
        self.canvas.delete("all")

        # Отрисовка подвинутого изображения
        for x_map in range(self.counter_x, min(len(self.array), self.counter_x + 47)):
            for y_map in range(self.counter_y, min(len(self.array[0]), self.counter_y + 27)):
                self.items.append(self.canvas.create_image(41 * (x_map - self.counter_x), 41 * (y_map- self.counter_y), anchor="nw", image=self.tk_im[self.array[x_map][y_map]]))

#-----------------------------------------------------------------------------Классы--------------------------------------------------------------------------

class square_map:

    # Инициалиация карты клеток
    def __init__(self, length, heigth, sizemap_x, sizemap_y):
        self.stock = []

        # Указание размера первичной карты
        for i in range(length + 2):
            useless = [square() for i in range(heigth + 2)]
            self.stock.append(useless)
        self.under_development = Queue()
        self.turn_cleaning = []
        self.interpolated_map = []

        # Указание размера аппроксимированной карты
        for i in range(sizemap_x):
            useless = [int() for j in range(sizemap_y)]
            self.interpolated_map.append(useless)

    # Поиск соседей клетки с координатами x, y
    def neighbours(self, x, y, step_x=1, step_y=1):
        res = []
        # Если сосед по х слева находится не на "противоположной" стороне карты, то:
        if (x - 1) * step_x > 0:
            # Проверка на диагональных соседей слева
            if (y - 1) * step_y > 0:
                res.append(((x - 1) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append(((x - 1) * step_x, (y + 1) * step_y))
            # Добавляем соседа слева
            res.append(((x - 1) * step_x, y * step_y))
        # А иначе:
        else:
            # Добавляем соседа слева
            res.append((((len(self.stock) - 2) // step_x) * step_x, y * step_y))
            # Проверка на диагональных соседей слева
            if (y - 1) * step_y > 0:
                res.append((((len(self.stock) - 2) // step_x) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append((((len(self.stock) - 2) // step_x) * step_x, (y + 1) * step_y))

        # Если сосед по х справа находится не на "противоположной" стороне карты, то:
        if (x + 1) * step_x < len(self.stock):
            # Проверка на диагональных соседей справа
            if (y - 1) * step_y > 0:
                res.append(((x + 1) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append(((x + 1) * step_x, (y + 1) * step_y))
            # Добавляем соседа справа
            res.append(((x + 1) * step_x, y * step_y))
        # А иначе:
        else:
            # Добавляем соседа справа
            res.append((step_x, y * step_y))
            # Проверка на диагональных соседей справа
            if (y - 1) * step_y > 0:
                res.append((step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append((step_x, (y + 1) * step_y))

        # Если сверху есть сосед, то добавим его
        if (y - 1) * step_y > 0:
            res.append((x * step_x, (y - 1) * step_y))
        # Если снизу есть сосед, то добавим его
        if (y + 1) * step_y < len(self.stock[0]):
            res.append((x * step_x, (y + 1) * step_y))
        return res

    # "Лопание" клетки с координатами x, y
    def pop(self, x, y, mode=1, delta_x=1, delta_y=1):
        # Узнаём наших соседей
        mates = self.neighbours(x, y, delta_x, delta_y)
        # Увеличиваем кол-во их посещений на 1 у каждого
        for coords in mates:
            if self.stock[coords[0]][coords[1]].count < 3: self.stock[coords[0]][coords[1]].count += mode
        return mates

    # Очистка клеток от "мусора"
    def clear(self, step_x = 1, step_y = 1):
        for i in range(1, ((len(self.stock) - 1) // step_x) + 1):
            for j in range(1, ((len(self.stock[0]) - 1) // step_y) + 1):
                self.stock[step_x * i][step_y * j].type = 0
                self.stock[step_x * i][step_y * j].count = 0
                self.stock[step_x * i][step_y * j].turn = 0

    # Вывод образов континента в консоль
    def show_continent(self, step_x = 1, step_y = 1):
        for i in range(1, ((len(self.stock) - 1) // step_x) + 1):
            for j in range(1, ((len(self.stock[0]) - 1) // step_y) + 1):
                print(self.stock[size_of_chunks_x * i][size_of_chunks_y * j].typeres, end=' ')
            print()
        print()

    # Отправка скорости взрывающейся клетки её соседям
    def send_speed(self, _from, _to, t, ground_level, speed_cut):
        # Считаем знак нащей функии
        value = sign(self.stock[_to[0]][_to[1]].speed + self.stock[_from[0]][_from[1]].speed +
                     random.randint(0, t - 1) - random.randint(0, t - 1) + (ground_level - self.stock[_from[0]][_from[1]].main))

        # Изменяем скорость роста высот в клетке-соседе по формуле ниже (игнорируя знак)
        self.stock[_to[0]][_to[1]].speed = ((value * (self.stock[_to[0]][_to[1]].speed + self.stock[_from[0]][_from[1]].speed +
                                            random.randint(0, t - 1) - random.randint(0, t - 1) + (ground_level - self.stock[_from[0]][_from[1]].main))) % speed_cut) * value

    # Аппроксимация высот карты
    def approximation(self):

        # Указываем размеры апрроксимируемых областей
        interpolation_x = len(self.stock) // (2 * len(self.interpolated_map))
        interpolation_y = len(self.stock[0]) // (2 * len(self.interpolated_map[0]))

        # Заполняем аппроксимированную карту высот
        for map_x in range(1, len(self.interpolated_map) + 1):
            for map_y in range(1, len(self.interpolated_map[0]) + 1):

                # Создаём счётчики клеток, встречающихся в каждой "области"
                counters = [0, 0, 0, 0, 0, 0]
                for x in range((2 * map_x - 2) * interpolation_x, (2 * map_x) * interpolation_x):
                    for y in range((2 * map_y - 2) * interpolation_y, (2 * map_y) * interpolation_y):
                        # Считаем, сколько клеток каждого типа встретилось на каждой из областей
                        counters[map.stock[x][y].id] += 1
                # Пишем id самой часто встречающейся клетки в соотвествующую клетку аппроксимированной карты высот
                self.interpolated_map[map_x - 1][map_y - 1] = counters.index(max(counters))

    # "Усредняем" высоту каждой из клеток
    def heigths_approximation(self):
        # Проходимся по всем клеткам карты
        for array in self.stock:
            for item in array:
                # Усредняем высоту по всем принятым значениям
                if item.delta > 0: item.heigth = item.heigth // item.delta

                # В зав-ти от высоты клетки, присваиваем ей свой "биом"
                if item.heigth <= 40: item.id = 0
                if item.heigth >= 41 and item.heigth <= 48: item.id = 5
                if item.heigth >= 49 and item.heigth <= 65: item.id = 1
                if item.heigth >= 66 and item.heigth <= 77: item.id = 2
                if item.heigth >= 78 and item.heigth <= 94: item.id = 3
                if item.heigth >= 95: item.id = 4

    # Убираем промежуточные значения из карты высот
    def clean_buffer(self):
        for guy in self.turn_cleaning:
            guy.turn = 0
            guy.count = 0
            guy.main = 0
            guy.speed = 0
        while not self.under_development.empty():
            self.under_development.get()
        self.turn_cleaning.clear()

    #----------------------------------------Смысловые функции--------------------------------------------

    def initialize_center(self, x, y):
        self.stock[x][y].count = 3
        self.stock[x][y].type = 1
        self.stock[x][y].typeres = random.randint(1, 2)
        self.stock[x][y].turn = 1

    def continent_tipisation(self, x, y):
        self.stock[x][y].type = 1
        if self.stock[x][y].typeres == 0:
            self.stock[x][y].typeres = random.randint(1, 2)
        else:
            self.stock[x][y].typeres = 3

    def popping_initialisation(self, coords, radius, counter):
        self.stock[coords[0]][coords[1]].main = (self.stock[coords[0]][coords[1]].main + self.stock[coords[0]][coords[1]].speed) // self.stock[coords[0]][coords[1]].count
        self.stock[coords[0]][coords[1]].speed = self.stock[coords[0]][coords[1]].speed // self.stock[coords[0]][coords[1]].count
        self.stock[coords[0]][coords[1]].delta += (radius - counter)
        self.stock[coords[0]][coords[1]].heigth += self.stock[coords[0]][coords[1]].main * (radius - counter)

    def biome_initialisation(self, center_x, center_y, normal, radius):
        self.stock[center_x][center_y].main = normal[self.stock[center_x][center_y].typeres]
        self.stock[center_x][center_y].turn = 1

        # Изменение итоговой высоты на значение, пропорциональное близости к центру генерации
        self.stock[center_x][center_y].heigth = self.stock[center_x][center_y].main * radius
        self.stock[center_x][center_y].delta += radius
        mates = self.pop(center_x, center_y, 3)
        for mate in mates:
            self.send_speed((center_x, center_y), mate, t, normal[self.stock[center_x][center_y].typeres], 20)
            self.stock[mate[0]][mate[1]].main = self.stock[center_x][center_y].main * 3
            self.stock[mate[0]][mate[1]].speed *= 3
            self.stock[mate[0]][mate[1]].turn = 1
            self.under_development.put(mate)
            self.turn_cleaning.append(self.stock[mate[0]][mate[1]])

        self.stock[center_x][center_y].count = 4
        self.stock[center_x][center_y].main = 0
        self.stock[center_x][center_y].speed = 0

    def add_to_development(self, mate):
        self.stock[mate[0]][mate[1]].turn = 1
        self.under_development.put(mate)
        self.turn_cleaning.append(self.stock[mate[0]][mate[1]])

    def speed_parameters_choosing(self, center_x, center_y, coords, mate, t, normal):

        # Если биом водный, то
        if self.stock[center_x][center_y].typeres == 0:

            # 3 условия на высоту "лопнувшего" соседа, меняющих режим генерации клетки
            if self.stock[coords[0]][coords[1]].main < 40:
                self.send_speed(coords, mate, t, normal[0], 20)
            elif self.stock[coords[0]][coords[1]].main < 48:
                self.send_speed(coords, mate, t, 45, 20)
            elif self.stock[coords[0]][coords[1]].main >= 48:
                self.send_speed(coords, mate, t, normal[1], 2000)

        # Если биом равнинный, то
        if self.stock[center_x][center_y].typeres == 1:

            # 3 условия на высоту "лопнувшего" соседа, меняющих режим генерации клетки
            if self.stock[coords[0]][coords[1]].main <= 48:
                self.send_speed(coords, mate, t, 43, 20)
            elif self.stock[coords[0]][coords[1]].main <= 65:
                self.send_speed(coords, mate, t, normal[1], 20)
            elif self.stock[coords[0]][coords[1]].main > 65:
                self.send_speed(coords, mate, t, normal[2], 20)

        # Если биом лесной, то
        if self.stock[center_x][center_y].typeres == 2:

            # 3 условия на высоту "лопнувшего" соседа, меняющих режим генерации клетки
            if self.stock[coords[0]][coords[1]].main <= 53:
                self.send_speed(coords, mate, t, 45, 20)
            elif self.stock[coords[0]][coords[1]].main <= 85:
                self.send_speed(coords, mate, t, normal[2], 20)
            elif self.stock[coords[0]][coords[1]].main > 85:
                self.send_speed(coords, mate, t, normal[3], 20)

        # Если биом горный, то
        if self.stock[center_x][center_y].typeres == 3:
            self.send_speed(coords, mate, t, normal[3], 30)



class square:
    def __init__(self):
        # Скорость "роста высоты" клетки
        self.speed = int()
        # Высота клетки в каком-то определённом чанке
        self.main = int()
        # Количество "посещений" клетки
        self.count = int()
        # Тип поверхнсти, которая будет располагаться на клетке
        self.id = int()
        # Итоговая (средняя) высота клетки по всем чанкам, с учётом близости от центров генераций
        self.heigth = int()
        # Лопнула ли ещё эта клетка при генерации конкретного чанка?
        self.turn = int()
        # "Вес", на который нужно делить self.heigth, для получения средней высоты
        self.delta = int()
        # Является ли генерируемый чанк - чанком суши?
        self.type = int()
        # Тип "биома", по которому бедет генерироваться чанк
        self.typeres = int()

#--------------------------------------------------------------------------------Функции----------------------------------------------------------------------

def sign(num):
    return -1 if num < 0 else 1

# Генерация одного континента
def continent_generate(map, center_x, center_y, size_of_chunks_x, size_of_chunks_y, continent_size):
    # Инициализация очереди обработки
    under_development = Queue()
    under_development.put((size_of_chunks_x * center_x, size_of_chunks_y * center_y))

    # Инициализация счётчиков
    size_of_generated_continent = 0
    number_of_targets = 0

    # Генерируем континент
    while size_of_generated_continent < continent_size:
        size_of_queue = under_development.qsize()

        # Идём по всем обрабатываемым центрам генерации суши
        for i in range(size_of_queue):

            # Инициализация данных, используемых далее, и счётчиков
            number_of_targets += 1
            rand = random.randint(0, 100)
            counter = 0

            # Работаем с "лопающейся" клеткой
            coords = under_development.get()
            mates = map.pop(coords[0] // size_of_chunks_x, coords[1] // size_of_chunks_y, 1, size_of_chunks_x, size_of_chunks_y)

            # Работа с соседями лопающейся клетки
            for mate in mates:
                if map.stock[mate[0]][mate[1]].type == 1:
                    counter += 1
                if map.stock[mate[0]][mate[1]].turn == 0 and map.stock[mate[0]][mate[1]].count >= 3:
                    under_development.put(mate)
                    map.stock[mate[0]][mate[1]].turn = 1

            # Работа непосредственно с лопающейся клуткой
            if map.stock[coords[0]][coords[1]].type == 0:
                if rand < counter * 28: map.continent_tipisation(coords[0], coords[1])

        # Увеличиваем счётчик размера континента
        size_of_generated_continent += 1

# Генерация всех образов континентов
def generate_map_of_continents(map, size_of_chunks_x, size_of_chunks_y, number_of_chunks_x, number_of_chunks_y, number_of_continents, size):

    numof_generated_ccntinents = 0
    while numof_generated_ccntinents < number_of_continents:

        # Ищем центр генерируемого континента
        rand_x = random.randint(1, number_of_chunks_x)
        rand_y = random.randint(1, number_of_chunks_y)
        if map.stock[size_of_chunks_x * rand_x][size_of_chunks_y * rand_y].typeres == 0:

            # Инициализируем центр континента
            map.initialize_center(size_of_chunks_x * rand_x, size_of_chunks_y * rand_y)

            # Собираем прямых соседей выбранного центра генерации
            mates = map.pop(rand_x, rand_y, 2, size_of_chunks_x, size_of_chunks_y)

            # Работа с прямыми соседями
            for mate in mates:
                rand = random.randint(1, 50) + random.randint(1, 50)
                # Заполняем соседей данными о посещаемости и типе биома
                if rand < 85: map.continent_tipisation(mate[0], mate[1])

            # Генерируем континент
            continent_generate(map, rand_x, rand_y, size_of_chunks_x, size_of_chunks_y, size)

            # Обнуляем все поля генерации для их дальнейшего заполнения
            map.clear(size_of_chunks_x, size_of_chunks_y)

            # Увеличиваем количество континентов
            numof_generated_ccntinents += 1

# Генерация рельефа в конкретном биоме
def generate_chunk(map, center_x, center_y, radius, normal, t):
    counter = 0
    while counter < radius:
        size_of_queue = map.under_development.qsize()

        # Идём по "радиусу" лопнутых клеток
        for n in range(size_of_queue):
            # Узнаём, какую клетку сейчас нужно "лопнуть"
            coords = map.under_development.get()

            # Заполнение "лопающейся" клетки
            map.popping_initialisation(coords, radius, counter)

            # Лопаем клетку
            mates = map.pop(coords[0], coords[1])

            # Идём по соседям лопающейся клетки
            for mate in mates:
                # Проверяем, не "лопнул" ли сосед клетки раньше?
                if map.stock[mate[0]][mate[1]].turn == 0:

                    # Увеличиваем высоту соседа "лопающейся" клетки
                    map.stock[mate[0]][mate[1]].main += map.stock[coords[0]][coords[1]].main

                    # Если клетка получила данные с как минимум трёх соседей, то на "лопается" (добавляется к обрабатываемым)
                    if map.stock[mate[0]][mate[1]].count >= 3: map.add_to_development(mate)

                    # В зависимости от типа местности, передаём сосседям разную скорость изменения высоты
                    map.speed_parameters_choosing(center_x, center_y, coords, mate, t, normal)

            # Чистим "лопнутого" соседа
            map.stock[coords[0]][coords[1]].main = 0
            map.stock[coords[0]][coords[1]].speed = 0
        counter += 1
    # Чистим все системные значения, для следующих итераций.
    map.clean_buffer()

# Генерация рельефа на всей карте
def generate_landscape(map, number_of_chunks_x, number_of_chunks_y, normal, t):

    # Идём по всем чанкам
    for i in range(1, number_of_chunks_x + 1):
        for j in range(1, number_of_chunks_y + 1):
            # Считаем расстояние, до которого будут генерироваться очаги генерации
            radius = max((2 * (len(map.stock) // (number_of_chunks_x + 1)) + 8), (2 * (len(map.stock[0]) // (number_of_chunks_y + 1)) + 8))

            center_x = i * size_of_chunks_x
            center_y = j * size_of_chunks_y

            # Игнициализируем центр чанка
            map.biome_initialisation(center_x, center_y, normal, radius)

            # Генерируем "чанк"
            generate_chunk(map, center_x, center_y, radius, normal, t)

# Cохранение массива высот в txt файле filename
def write_map_array(stock, filename):

    # Создаём отдельный файл filename.txt
    file = open(filename + '.txt', 'w')

    # Пишем размер карты первыми 2 цифрами в файл
    file.write(str(len(stock)) + ' ' + str(len(stock[0])) + '\n')

    output = ""
    # Записываем каждую высоту в filename.txt
    for x in range(len(stock)):
        for y in range(len(stock[0])):
            output += str(stock[x][y]) + " "
        file.write(output + '\n')
        output = ""

#--------------------------------------------------------------------------------Константы-----------------------------------------------------------------------

# Средние высоты биомов
normal = [15, 59, 71, 96]
# Разброс скорости генерации
t = 11

# Размер Континента
size = 20

#----------------------------------------------------------------------------Тело программы----------------------------------------------------------------------

# Итоговая лина карты
sizemap_x = int(input())
# Итоговая ширина карты
sizemap_y = int(input())
# Кол-во генерируемых континентов (Если карта маленькая, а континентов оч много - error)
number_of_continents = int(input())
# Название файла, в который будет записываться карта высот
filename = str(input())

# Длина карты до аппроксимации
length = sizemap_x * 4
# Высота карты до аппроксимации
heigth = sizemap_y * 4
number_of_chunks_x = length // 25
number_of_chunks_y = heigth // 25

# Задаём необходимый размер карты
map = square_map(length, heigth, sizemap_x, sizemap_y)

size_of_chunks_x = length // (number_of_chunks_x + 1)
size_of_chunks_y = heigth // (number_of_chunks_y + 1)
numof_generated_ccntinents = 0

# Генерируем карту континентов
generate_map_of_continents(map, size_of_chunks_x, size_of_chunks_y, number_of_chunks_x, number_of_chunks_y, number_of_continents, size)

# Уведомляем об успешном размещении материков на образе карты
print("Generating_started")

# Генерируем высоты континента
generate_landscape(map, number_of_chunks_x, number_of_chunks_y, normal, t)

# Аппроксимация высот карты
map.heigths_approximation()

# Аппроксимация клеток карты
map.approximation()

write_map_array(map.interpolated_map, filename)

# Работаем с окном вывода программы
root = tk.Tk()
root.title("Генератор карт")
app = ExampleApp(root, map.interpolated_map)
if sys.platform != 'linux2':
    root.wm_state('zoomed')
else:
    root.wm_attributes('-zoomed', True)
root.mainloop()
