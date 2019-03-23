import arcade


class GameField:
    def __init__(self, size_in_pixels, size):
        self.size = size
        self.size_in_pixels = size_in_pixels // size * size
        base_list = [None] * size
        self.base_list = [base_list] * size
        self.cell_size = size_in_pixels // size

    def print_field_info(self):
        for i in self.base_list:
            print(i)

    def draw_field(self):
        for i in range(self.size + 1):
            arcade.draw_line(10 + self.cell_size * i,        # vertical lines
                             100,
                             10 + self.cell_size * i,
                             100 + self.size_in_pixels,
                             color=arcade.color.BLACK, line_width=3)
            arcade.draw_line(10,                             # horizontal line
                             100 + self.cell_size * i,
                             10 + self.size_in_pixels,
                             100 + self.cell_size * i,
                             color=arcade.color.BLACK, line_width=3)
