#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from Multiplayer import Client_game
import arcade


def enter_name(sock):
    name = input()
    sock.send(bytes(name, "UTF-8"))  # посылаем введенное имя на сервер
    check = sock.recv(1024).decode()  # получаем ответ от сервера

    while check == 'This fraction name is already taken':  # если имя уже занято повторяем попытку ввода
        print(check)
        name = input()
        sock.send(bytes(name, "UTF-8"))
        check = sock.recv(1024).decode()
    print(check)


def start_game(sock):
    game = Client_game.MyGame(sock)
    game.setup()
    arcade.run()


def main():
    sock = socket.socket()
    sock.connect(('localhost', 9090))

    connected = sock.recv(1024)  # получаем подтверждение подключения
    print(connected.decode())

    enter_name(sock)  # вводим имя фракции

    start = sock.recv(1024).decode()
    if start == 'start':
        start_game(sock)

    sock.close()  # закрываем соединение


if __name__ == "__main__":
    main()
