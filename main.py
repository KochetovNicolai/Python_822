#!/usr/bin/env python

from __future__ import print_function
import random
from queue import Queue
import tkinter as tk
from PIL import Image, ImageTk

class ExampleApp(tk.Tk):

    def _draw_image_left(self, event):
        self.items.clear()
        self.tk_im.clear()
        self.canvas.delete("all")
        if self.counter_x > 0: self.counter_x -= 1
        for x_map in range(self.counter_x, min(len(self.array), self.counter_x + 47)):
            for y_map in range(self.counter_y, min(len(self.array[0]), self.counter_y + 27)):
                if self.array[x_map][y_map] == 0: self.im = Image.open('Water_deep.png')
                if self.array[x_map][y_map] == 1: self.im = Image.open('Plains.png')
                if self.array[x_map][y_map] == 2: self.im = Image.open('Forests.png')
                if self.array[x_map][y_map] == 3: self.im = Image.open('Mountains.png')
                if self.array[x_map][y_map] == 4: self.im = Image.open('Snowy_mountains.png')
                if self.array[x_map][y_map] == 5: self.im = Image.open('Water_not_deep.png')
                self.tk_im.append(ImageTk.PhotoImage(self.im))
                self.items.append(self.canvas.create_image(41 * (x_map - self.counter_x), 41 * (y_map- self.counter_y), anchor="nw", image=self.tk_im[len(self.tk_im) - 1]))
    def _draw_image_right(self, event):
        self.items.clear()
        self.tk_im.clear()
        self.canvas.delete("all")
        self.counter_x += 1
        for x_map in range(self.counter_x, min(len(self.array), self.counter_x + 47)):
            for y_map in range(self.counter_y, min(len(self.array[0]), self.counter_y + 27)):
                if self.array[x_map][y_map] == 0: self.im = Image.open('Water_deep.png')
                if self.array[x_map][y_map] == 1: self.im = Image.open('Plains.png')
                if self.array[x_map][y_map] == 2: self.im = Image.open('Forests.png')
                if self.array[x_map][y_map] == 3: self.im = Image.open('Mountains.png')
                if self.array[x_map][y_map] == 4: self.im = Image.open('Snowy_mountains.png')
                if self.array[x_map][y_map] == 5: self.im = Image.open('Water_not_deep.png')
                self.tk_im.append(ImageTk.PhotoImage(self.im))
                self.items.append(self.canvas.create_image(41 * (x_map - self.counter_x), 41 * (y_map- self.counter_y), anchor="nw", image=self.tk_im[len(self.tk_im) - 1]))
    def _draw_image_up(self, event):
        self.items.clear()
        self.tk_im.clear()
        self.canvas.delete("all")
        if self.counter_y > 0: self.counter_y -= 1
        for x_map in range(self.counter_x, min(len(self.array), self.counter_x + 47)):
            for y_map in range(self.counter_y, min(len(self.array[0]), self.counter_y + 27)):
                if self.array[x_map][y_map] == 0: self.im = Image.open('Water_deep.png')
                if self.array[x_map][y_map] == 1: self.im = Image.open('Plains.png')
                if self.array[x_map][y_map] == 2: self.im = Image.open('Forests.png')
                if self.array[x_map][y_map] == 3: self.im = Image.open('Mountains.png')
                if self.array[x_map][y_map] == 4: self.im = Image.open('Snowy_mountains.png')
                if self.array[x_map][y_map] == 5: self.im = Image.open('Water_not_deep.png')
                self.tk_im.append(ImageTk.PhotoImage(self.im))
                self.items.append(self.canvas.create_image(41 * (x_map - self.counter_x), 41 * (y_map- self.counter_y), anchor="nw", image=self.tk_im[len(self.tk_im) - 1]))
    def _draw_image_down(self, event):
        self.items.clear()
        self.tk_im.clear()
        self.canvas.delete("all")
        self.counter_y += 1
        for x_map in range(self.counter_x, min(len(self.array), self.counter_x + 47)):
            for y_map in range(self.counter_y, min(len(self.array[0]), self.counter_y + 27)):
                if self.array[x_map][y_map] == 0: self.im = Image.open('Water_deep.png')
                if self.array[x_map][y_map] == 1: self.im = Image.open('Plains.png')
                if self.array[x_map][y_map] == 2: self.im = Image.open('Forests.png')
                if self.array[x_map][y_map] == 3: self.im = Image.open('Mountains.png')
                if self.array[x_map][y_map] == 4: self.im = Image.open('Snowy_mountains.png')
                if self.array[x_map][y_map] == 5: self.im = Image.open('Water_not_deep.png')
                self.tk_im.append(ImageTk.PhotoImage(self.im))
                self.items.append(self.canvas.create_image(41 * (x_map - self.counter_x), 41 * (y_map- self.counter_y), anchor="nw", image=self.tk_im[len(self.tk_im) - 1]))

    def __init__(self, master, array):
        self.array = array
        self.x = self.y = 0
        self.tk_im = []
        self.counter_x = self.counter_y = 0
        self.step = 0
        self.items = []
        self.canvas = tk.Canvas(master, width=512, height=512, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        button1 = tk.Button(self.canvas, text= "Up")
        button1.bind("<Button-1>", self._draw_image_up)
        button1.pack(side="bottom")
        button2 = tk.Button(self.canvas, text="Down")
        button2.bind("<Button-1>", self._draw_image_down)
        button2.pack(side="bottom")
        button3 = tk.Button(self.canvas, text="Left")
        button3.bind("<Button-1>", self._draw_image_left)
        button3.pack(side="bottom")
        button4 = tk.Button(self.canvas, text="Right")
        button4.bind("<Button-1>", self._draw_image_right)
        button4.pack(side="bottom")

        self._draw_image()

    def _draw_image(self):
        self.items.clear()
        self.tk_im.clear()
        for x_map in range(self.counter_x, min(len(self.array), self.counter_x + 47)):
            for y_map in range(self.counter_y, min(len(self.array[0]), self.counter_y + 27)):
                if self.array[x_map][y_map] == 0: self.im = Image.open('Water_deep.png')
                if self.array[x_map][y_map] == 1: self.im = Image.open('Plains.png')
                if self.array[x_map][y_map] == 2: self.im = Image.open('Forests.png')
                if self.array[x_map][y_map] == 3: self.im = Image.open('Mountains.png')
                if self.array[x_map][y_map] == 4: self.im = Image.open('Snowy_mountains.png')
                if self.array[x_map][y_map] == 5: self.im = Image.open('Water_not_deep.png')
                self.tk_im.append(ImageTk.PhotoImage(self.im))
                self.items.append(self.canvas.create_image(41 * x_map, 41 * y_map, anchor="nw", image=self.tk_im[len(self.tk_im) - 1]))

#-----------------------------------------------------------------------Классы---------------------------------------------------------------

class square_map:
    def __init__(self, length, heigth, sizemap_x, sizemap_y):
        self.stock = []
        for i in range(length + 2):
            useless = [square() for i in range(heigth + 2)]
            self.stock.append(useless)
        self.under_development = Queue()
        self.turn_cleaning = []
        self.interpolated_map = []
        for i in range(sizemap_x):
            useless = [int() for j in range(sizemap_y)]
            self.interpolated_map.append(useless)

    def neighbours(self, x, y, step_x=1, step_y=1):
        res = []
        if (x - 1) * step_x > 0:
            if (y - 1) * step_y > 0:
                res.append(((x - 1) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append(((x - 1) * step_x, (y + 1) * step_y))
            res.append(((x - 1) * step_x, y * step_y))
        else:
            res.append((((len(self.stock) - 2) // step_x) * step_x, y * step_y))
            if (y - 1) * step_y > 0:
                res.append((((len(self.stock) - 2) // step_x) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append((((len(self.stock) - 2) // step_x) * step_x, (y + 1) * step_y))
        if (x + 1) * step_x < len(self.stock):
            if (y - 1) * step_y > 0:
                res.append(((x + 1) * step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append(((x + 1) * step_x, (y + 1) * step_y))
            res.append(((x + 1) * step_x, y * step_y))
        else:
            res.append((step_x, y * step_y))
            if (y - 1) * step_y > 0:
                res.append((step_x, (y - 1) * step_y))
            if (y + 1) * step_y < len(self.stock[0]):
                res.append((step_x, (y + 1) * step_y))
        if (y - 1) * step_y > 0:
            res.append((x * step_x, (y - 1) * step_y))
        if (y + 1) * step_y < len(self.stock[0]):
            res.append((x * step_x, (y + 1) * step_y))
        return res

    def pop(self, x, y, mode=1, delta_x=1, delta_y=1):
        mates = self.neighbours(x, y, delta_x, delta_y)
        for coords in mates:
            try:
                if self.stock[coords[0]][coords[1]].count < 3:
                    self.stock[coords[0]][coords[1]].count += mode
            except:
                print(coords[0])
                print(coords[1])
                exit(0)
        return mates

    def continent_tipisation(self, x, y):
        self.stock[x][y].type = 1
        if self.stock[x][y].typeres == 0:
            self.stock[x][y].typeres = random.randint(1, 2)
        else:
            self.stock[x][y].typeres = 3

    def initialize_center(self, x, y):
        self.stock[x][y].count = 3
        self.stock[x][y].type = 1
        self.stock[x][y].typeres = random.randint(1, 2)
        self.stock[x][y].turn = 1

    def clear(self, step_x = 1, step_y = 1):
        for i in range(1, ((len(self.stock) - 1) // step_x) + 1):
            for j in range(1, ((len(self.stock[0]) - 1) // step_y) + 1):
                self.stock[step_x * i][step_y * j].type = 0
                self.stock[step_x * i][step_y * j].count = 0
                self.stock[step_x * i][step_y * j].turn = 0

    def show_continent(self, step_x = 1, step_y = 1):
        for i in range(1, ((len(self.stock) - 1) // step_x) + 1):
            for j in range(1, ((len(self.stock[0]) - 1) // step_y) + 1):
                print(self.stock[size_of_chunks_x * i][size_of_chunks_y * j].typeres, end=' ')
            print()
        print()

    def send_speed(self, _from, _to, t, ground_level, speed_cut):
        value = sign(self.stock[_to[0]][_to[1]].speed + self.stock[_from[0]][_from[1]].speed +
                     random.randint(0, t - 1) - random.randint(0, t - 1) + (ground_level - self.stock[_from[0]][_from[1]].main))
        self.stock[_to[0]][_to[1]].speed = ((value * (self.stock[_to[0]][_to[1]].speed + self.stock[_from[0]][_from[1]].speed +
                                            random.randint(0, t - 1) - random.randint(0, t - 1) + (ground_level - self.stock[_from[0]][_from[1]].main))) % speed_cut) * value

class square:
    def __init__(self):
        self.speed = int()
        self.main = int()
        self.count = int()
        self.id = bool()
        self.heigth = int()
        self.turn = int()
        self.delta = int()
        self.type = int()
        self.typeres = int()
        self.middle = int()
        self.normal = int()

#--------------------------------------------------------------------------------Функции----------------------------------------------------------------------

def sign(num):
    return -1 if num < 0 else 1

def continent_generate(map, center_x, center_y, size_of_chunks_x, size_of_chunks_y, continent_size):
    under_development = Queue()
    under_development.put((size_of_chunks_x * center_x, size_of_chunks_y * center_y))
    size_of_generated_continent = 0

    # Генерируем континент
    while size_of_generated_continent < continent_size:
        size_of_queue = under_development.qsize()

        # Идём по всем обрабатываемым центрам генерации суши
        for i in range(size_of_queue):
            rand = random.randint(0, 100)
            counter = 0
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

        # Увеличиваем счётчик сгенерированных континентов
        size_of_generated_continent += 1

#--------------------------------------------------------------------------------Константы--------------------------------------------------------------------

normal = [15, 59, 71, 96]
t = 11
u = 11

t1 = 17
u1 = 5

u2 = 8
t2 = 15

t3 = 5
u3 = 1

#Размер Континента
size = 20

#----------------------------------------------------------------------------Тело программы-----------------------------------------------------------

#Итоговая лина карты
sizemap_x = int(input())
#Итоговая ширина карты
sizemap_y = int(input())
#Кол-во генерируемых континентов (Если карта маленькая, а континентов оч много - error)
number_of_continents = int(input())

#Длина карты до аппроксимации
length = sizemap_x * 4
#Высота карты до аппроксимации
heigth = sizemap_y * 4
number_of_chunks_x = length // 25
number_of_chunks_y = heigth // 25

#Задаём необходимый размер карты
map = square_map(length, heigth, sizemap_x, sizemap_y)

size_of_chunks_x = length // (number_of_chunks_x + 1)
size_of_chunks_y = heigth // (number_of_chunks_y + 1)
numof_generated_ccntinents = 0

#Пишем генерацию континентов
while numof_generated_ccntinents < number_of_continents:
    rand_x = random.randint(1, number_of_chunks_x)
    rand_y = random.randint(1, number_of_chunks_y)
    if map.stock[size_of_chunks_x * rand_x][size_of_chunks_y * rand_y].typeres == 0:

        #Инициализируем центр континента
        map.initialize_center(size_of_chunks_x * rand_x, size_of_chunks_y * rand_y)

        #Собираем прямых соседей выбранного центра генерации
        mates = map.pop(rand_x, rand_y, 2, size_of_chunks_x, size_of_chunks_y)

        #Работа с прямыми соседями
        for mate in mates:
            rand = random.randint(1, 50) + random.randint(1, 50)
            #Заполняем соседей данными о посещаемости и типе биома
            if rand < 85: map.continent_tipisation(mate[0], mate[1])

        #Генерируем континент
        continent_generate(map, rand_x, rand_y, size_of_chunks_x, size_of_chunks_y, size)

        #Обнуляем все поля генерации для их дальнейшего заполнения
        map.clear(size_of_chunks_x, size_of_chunks_y)

        #Выводим результат работы программы
        #map.show_continent(size_of_chunks_x, size_of_chunks_y)

        #Увеличиваем количество континентов
        numof_generated_ccntinents += 1

#--------------------------------------------------------Генерация континента завершена--------------------------------------------------------------

for i in range(1, number_of_chunks_x + 1):
    for j in range(1, number_of_chunks_y + 1):
        center_x = i * size_of_chunks_x
        center_y = j * size_of_chunks_y
        #print(center_y)
        try:
            map.stock[center_x][center_y].speed = random.randint(0, t - 1) - random.randint(0, t - 1)
        except:
            #print(i, size_of_chunks_x)
            #print(j, size_of_chunks_y, number_of_chunks)
            exit(0)
        if j > 7:
            useful = 0
        map.stock[center_x][center_y].main = normal[map.stock[center_x][center_y].typeres]
        map.stock[center_x][center_y].turn = 1

        #Расстояние, до которого будут генерироваться очаги генерации
        radius = max((2 * (length // (number_of_chunks_x + 1)) + 8), (2 * (heigth // (number_of_chunks_y + 1)) + 8))

        #Изменение итоговой высоты на значение, пропорциональное близости к центру генерации
        map.stock[center_x][center_y].heigth = map.stock[center_x][center_y].main * radius
        map.stock[center_x][center_y].delta += radius
        mates = map.pop(center_x, center_y, 3)
        for mate in mates:
            map.send_speed((center_x, center_y), mate, t, normal[map.stock[center_x][center_y].typeres], 20)
            map.stock[mate[0]][mate[1]].main = map.stock[center_x][center_y].main * 3
            map.stock[mate[0]][mate[1]].speed *= 3
            map.stock[mate[0]][mate[1]].turn = 1
            map.under_development.put(mate)
            map.turn_cleaning.append(map.stock[mate[0]][mate[1]])

        map.stock[center_x][center_y].count = 4
        map.stock[center_x][center_y].main = 0
        map.stock[center_x][center_y].speed = 0
        counter = 0
        while counter < radius:
            size_of_queue = map.under_development.qsize()
            for n in range(size_of_queue):
                coords = map.under_development.get()
                map.stock[coords[0]][coords[1]].main = (map.stock[coords[0]][coords[1]].main + map.stock[coords[0]][coords[1]].speed) // map.stock[coords[0]][coords[1]].count
                map.stock[coords[0]][coords[1]].speed = map.stock[coords[0]][coords[1]].speed // map.stock[coords[0]][coords[1]].count
                map.stock[coords[0]][coords[1]].delta += (radius - counter)
                map.stock[coords[0]][coords[1]].heigth += map.stock[coords[0]][coords[1]].main * (radius - counter)

                mates = map.pop(coords[0], coords[1])
                for mate in mates:
                    if map.stock[mate[0]][mate[1]].turn == 0:
                        map.stock[mate[0]][mate[1]].main += map.stock[coords[0]][coords[1]].main
                        if map.stock[mate[0]][mate[1]].count >= 3:
                            map.stock[mate[0]][mate[1]].turn = 1
                            map.under_development.put(mate)
                            map.turn_cleaning.append(map.stock[mate[0]][mate[1]])

                        if map.stock[center_x][center_y].typeres == 0:
                            if map.stock[coords[0]][coords[1]].main < 40:
                                map.send_speed(coords, mate, t, normal[0], 20)
                            if map.stock[coords[0]][coords[1]].main >= 40 and map.stock[coords[0]][coords[1]].main < 48:
                                map.send_speed(coords, mate, t, 45, 2000)
                            if map.stock[coords[0]][coords[1]].main >= 48:
                                map.send_speed(coords, mate, t, normal[1], 20)
                        if map.stock[center_x][center_y].typeres == 1:
                            if map.stock[coords[0]][coords[1]].main <= 48:
                                map.send_speed(coords, mate, t, 43, 20)
                            elif map.stock[coords[0]][coords[1]].main <= 65:
                                map.send_speed(coords, mate, t, normal[1], 20)
                            elif map.stock[coords[0]][coords[1]].main > 65:
                                map.send_speed(coords, mate, t, normal[2], 20)
                        if map.stock[center_x][center_y].typeres == 2:
                            if map.stock[coords[0]][coords[1]].main <= 53:
                                map.send_speed(coords, mate, t, 45, 20)
                            elif map.stock[coords[0]][coords[1]].main <= 85:
                                map.send_speed(coords, mate, t, normal[2], 20)
                            elif map.stock[coords[0]][coords[1]].main > 85:
                                map.send_speed(coords, mate, t, normal[3], 20)
                        if map.stock[center_x][center_y].typeres == 3:
                            map.send_speed(coords, mate, t, normal[3], 30)
                map.stock[coords[0]][coords[1]].main = 0
                map.stock[coords[0]][coords[1]].speed = 0
            counter += 1
            #print(map.under_development.qsize())
        for guy in map.turn_cleaning:
            guy.turn = 0
            guy.count = 0
            guy.main = 0
            guy.speed = 0
        while not map.under_development.empty():
            map.under_development.get()
        map.turn_cleaning.clear()
#--------------------------------------------------------------Аппроксимация высот карты-------------------------------------------------------

for array in map.stock:
    for item in array:
        if item.delta > 0: item.heigth = item.heigth // item.delta
        if item.heigth <= 40: item.id = 0
        if item.heigth >= 41 and item.heigth <= 48: item.id = 5
        if item.heigth >= 49 and item.heigth <= 65: item.id = 1
        if item.heigth >= 66 and item.heigth <= 77: item.id = 2
        if item.heigth >= 78 and item.heigth <= 94: item.id = 3
        if item.heigth >= 95: item.id = 4

interpolation_x = length // (2 * sizemap_x)
interpolation_y = heigth // (2 * sizemap_y)

#---------------------------------------------------------------Аппроксимация клеток карты------------------------------------------------------

for map_x in range(1, sizemap_x + 1):
    for map_y in range(1, sizemap_y + 1):
        counters = [0, 0, 0, 0, 0, 0]
        for x in range((2 * map_x - 2) * interpolation_x, (2 * map_x) * interpolation_x):
            for y in range((2 * map_y - 2) * interpolation_y, (2 * map_y) * interpolation_y):
                counters[map.stock[x][y].id] += 1
        map.stock[(2 * map_x - 1) * interpolation_x][(2 * map_y - 1) * interpolation_y].middle = counters.index(max(counters))
        map.interpolated_map[map_x - 1][map_y - 1] = map.stock[(2 * map_x - 1) * interpolation_x][(2 * map_y - 1) * interpolation_y].middle
#print(map.interpolated_map[0])
root = tk.Tk()
app = ExampleApp(root, map.interpolated_map)
root.mainloop()