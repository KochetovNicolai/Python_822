#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


def main():
    sock = socket.socket()
    sock.connect(('localhost', 9090))

    connected = sock.recv(1024)  # получаем подтверждение подключения
    print(connected.decode())

    name = input()
    sock.send(bytes(name, "UTF-8"))
    check = sock.recv(1024).decode()

    while check == 'This fraction name is already taken':
        print(check)
        name = input()
        sock.send(bytes(name, "UTF-8"))
        check = sock.recv(1024).decode()
    print(check)

    sock.close()


if __name__ == "__main__":
    main()
