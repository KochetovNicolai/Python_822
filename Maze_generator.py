import sys

from Maze import Maze
from generate_load import load_maze, generate
from solution import solution


if sys.argv[1] == 'load':  # первый аргумент - либо 'load', либо 'generate'
    try:
        maze = load_maze(sys.argv[2])
        print(maze)
    except Exception as e:
        maze = Maze(1, 1)
        print('\033[91m' + type(e).__name__ + '\033[0m', end='\n')
        print('WRONG LOADING FORMAT')
        raise SyntaxError
    # в этом случае 2й аргумент - название файла, из которого будет производиться загрузка
    # файл должен лежать в одной директории с проектом
elif sys.argv[1] == 'generate':
    maze = Maze(int(sys.argv[2]), int(sys.argv[3]))
    # а в этом случае 2й и 3й аргументы - размеры лабиринта, 4й - способ генерации: 'dfs' или 'prim'
    # 5й агрумент необязательный, говорит как сгенерировать вход и выход: 'rand' или 'not_rand'('not_rand' по умолч.)
    try:
        if len(sys.argv) > 5:
            generate(maze, sys.argv[4], sys.argv[5])
        else:
            generate(maze, sys.argv[4])
        print(maze)
    except Exception as e:
        maze = Maze(1, 1)
        print('\033[91m' + type(e).__name__ + '\033[0m', end='\n')
        print('NO SUCH ALGORITHM')
        raise SyntaxError
else:
    print('WRONG ARGUMENTS FORMAT')
    raise SyntaxError


while True:
    ask1 = input('Do you want to save the maze? [yes/no] ')
    if ask1 == 'yes':
        file1 = input('Please, enter the filename(with extension): ')
        maze.save(file1)
        break
    elif ask1 == 'no':
        file1 = ''
        break
    else:
        file1 = ''
        print('wrong answer-format')

ask2 = input('Do you want to see the solution? [yes/no] ')
while True:
    if ask2 == 'yes':
        maze1 = solution(maze)
        print(maze1)
        while True:
            ask2 = input('Do you want to save the solution? [yes/no] ')
            if ask2 == 'yes':
                file2 = input('Please, enter the filename(with extension): ')
                if file1 == file2:
                    maze1.save(file2, 'a')
                else:
                    maze1.save(file2, 'w')
                break
            elif ask2 == 'no':
                break
            else:
                print('wrong answer-format')
        break
    elif ask2 == 'no':
        break
    else:
        print('wrong answer-format')
