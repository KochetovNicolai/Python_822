import arcade


class GameField:
    def __init__(self, size_in_pixels, size):
        self.size = size
        self.size_in_pixels = size_in_pixels // size * size
        self.base_list = []
        self.field_info = [[None for i in range(size)] for j in range(size)]
        self.cell_size = size_in_pixels // size
        self.bottom_border = 100
        self.left_border = 10

    def print_field_info(self):
        for i in self.base_list:
            print(i)

    def draw_field(self):
        for i in range(self.size + 1):
            arcade.draw_line(self.left_border + self.cell_size * i,        # vertical lines
                             self.bottom_border,
                             self.left_border + self.cell_size * i,
                             self.bottom_border + self.size_in_pixels,
                             color=arcade.color.BLACK_LEATHER_JACKET, line_width=3)
            arcade.draw_line(self.left_border,                             # horizontal line
                             self.bottom_border + self.cell_size * i,
                             self.left_border + self.size_in_pixels,
                             self.bottom_border + self.cell_size * i,
                             color=arcade.color.BLACK_LEATHER_JACKET, line_width=3)
