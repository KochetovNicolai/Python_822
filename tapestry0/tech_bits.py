# auxiliary implementations
from arcade import Sprite

import config
from config import CLASS_NAMES


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def type_validation(func, message=None, check=None):
    class Exc(Exception):
        pass

    flag = False
    while True:
        try:
            temp = func()
            if check is not None and not check(temp):
                raise Exc
            if flag:
                print("Ok!")
            return temp
        except ValueError:
            flag = True
            if check is None and message is not None:
                print(message)
            else:
                print(f"Wrong type - try again")
        except Exc:
            flag = True
            print(message)


class Dummy(Sprite, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.physics = self

    def update(self):
        self.kill()


def input_map_size():
    return type_validation(lambda: tuple(map(int, input().split())), message="Wrong size",
                           check=lambda x: len(x) == 2
                           and x[0] >= config.MAP_INPUT_LIMIT['x']
                           and x[1] >= config.MAP_INPUT_LIMIT['y'])


def input_number_of_players():
    return type_validation(lambda: int(input()), message="Wrong input - expected a single number")


def input_player_position():
    return type_validation(lambda: tuple(map(int, input().split())),
                           message="Wrong coordinates",
                           check=lambda x: len(x) == 2 and 0 <= x[0] < config.CELL_COUNT_X
                           and 0 <= x[1] < config.CELL_COUNT_Y)


def input_player_type():
    return type_validation(lambda: input(), message="Wrong class name",
                           check=lambda x: x in CLASS_NAMES)
