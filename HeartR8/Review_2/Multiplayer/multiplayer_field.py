import arcade


class GameField:
    def __init__(self, size):
        self.size = size
        self.base_list = []
        self.field_info = [[None for i in range(size)] for j in range(size)]
