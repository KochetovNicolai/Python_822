import socket
from multiprocessing import Process, Manager
import MyGame
import arcade


def enter_nickname(name_list, player, number_of_players, num):
    player.send(bytes("{} players connected, give name to your fraction:".format(number_of_players), "UTF-8"))  # просим игрока ввести ник
    name = player.recv(1024).decode()  # получаем ник от игрока
    name_entered = False  # выставляем флаг на "Ник не введен"
    while not name_entered:
        for i in name_list:  # Проходим по списку и проверяем, не введен ли уже такой ник
            if i[1] == name:
                name_entered = True
        if name_entered:  # Если введен -- посылаем игроку повторный запрос и получаем новый ник
            player.send(bytes('This fraction name is already taken', "UTF-8"))
            name = player.recv(1024).decode()
            name_entered = False
        else:  # Иначе посылаем игроку подтверждение вверного ввода и добавляем пару сокет_игрока-никнейм в список
            player.send(bytes('Nice fraction name!', "UTF-8"))
            name_list.append([num, name])
            name_entered = True


def enter_num_of_players():  # функция для верного ввода количества игроков с консоли
    print('Enter number of players')
    number_of_players = 0
    entered = False
    while not entered:
        try:
            number_of_players = int(input())
            if number_of_players > 1:
                entered = True
            else:
                print("There can be only 2 or more players in the game")
        except ValueError:
            print("Please enter number of players correctly")
            entered = False
    return number_of_players


def get_server_socket(number_of_players):  # получаение серверного сокета
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 9090))
    server.listen(number_of_players)
    return server


def main():
    number_of_players = enter_num_of_players()  # вводим количество игроков

    server = get_server_socket(number_of_players)  # создаем сокет сервера

    server_players_list = []  # список для сокетов
    player_list = [None] * number_of_players  # игровой список
    m = Manager()
    name_list = m.list()  # список имен фракций, заполняется игроками

    for i in range(number_of_players):  # устанавливаем соединения с игроками
        conn, addr = server.accept()
        print('connected:', addr)
        server_players_list.append(conn)

    procs = []  # список всех происходящих сейчас процессов

    for num, player in enumerate(server_players_list):  # делим работу на процессы, получаем имена фракций игроков
        proc = Process(target=enter_nickname, args=(name_list, player, number_of_players, num))
        procs.append(proc)
        proc.start()

    for proc in procs:  # ждем завершения всех процессов
        proc.join()

    print(name_list)  # выводим список имен игроков вместе с соответствующим номером игрока
    names = [None] * number_of_players

    for i in name_list:  # записываем никнеймы в новый список в правильном порядке
        names[i[0]] = i[1]

    print(names)

    field_size = 10

    game = MyGame.MyGame(field_size, player_list, names)
    game.setup()
    arcade.run()

    for conn in server_players_list:  # закрываем все соединения
        conn.close()


if __name__ == "__main__":
    main()
