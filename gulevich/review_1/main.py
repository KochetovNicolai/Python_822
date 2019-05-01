import sys

from generate_load import load_maze, generate
from solution import solution


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == 'load':  # первый аргумент - либо 'load', либо 'generate'
        try:
            maze = load_maze()
            print(maze)
        except Exception as e:
            print('\033[91m' + type(e).__name__ + '\033[0m', end='\n')
            print(e)
            raise SystemExit(777)
        # в этом случае 2й аргумент - название файла, из которого будет производиться загрузка
        # файл должен лежать в одной директории с проектом
    elif len(sys.argv) >= 2 and sys.argv[1] == 'generate':
        # а в этом случае 2й и 3й аргументы - размеры лабиринта, 4й - способ генерации: 'dfs' или 'prim'
        # 5й агрумент необязательный, говорит как сгенерировать вход и выход: 'rand' или 'not_rand'('not_rand' по умолч)
        if len(sys.argv) < 4:
            print('Введите в качестве 2, 3 и 4 аргументов параметры генерации')
            raise SystemExit(777)
        try:
            if len(sys.argv) > 5:
                maze = generate(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
            else:
                maze = generate(sys.argv[2], sys.argv[3], sys.argv[4])
            print(maze)
        except Exception as e:
            print('\033[91m' + type(e).__name__ + '\033[0m', end='\n')
            print(e)
            raise SystemExit(777)
    else:
        print('В качестве первого аргумента укажите, как вы хотите построить лабиринт: load или generate')
        raise SystemExit(777)

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
            if maze1 is False:
                print('NO SOLUTION')
            else:
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
