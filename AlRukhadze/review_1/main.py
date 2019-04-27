import pygame
import game

pygame.init()   # инициализация всех модулей библиотеки

pygame.display.set_caption("15 Puzzle")  # заголовок окна


def main():
    mygame = game.Game()
    mygame.start()


if __name__ == '__main__':  # выполняется, если модуль был запущен, как самостоятельный
    main()
