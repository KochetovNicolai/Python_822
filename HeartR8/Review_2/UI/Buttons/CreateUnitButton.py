from UI.Buttons.TextButton import TextButton


class CreateUnitButton(TextButton):
    def __init__(self, center_x, center_y, size_x, size_y, action_function, unit_type, text, cell_size, base_position):
        super().__init__(center_x, center_y, size_x, size_y, text, 18, "Arial")
        self.action_function = action_function
        self.unit_type = unit_type
        self.cell_size = cell_size
        self.base_position = base_position

    def on_press(self):
        super().on_press()
        self.action_function(self.unit_type, self.cell_size, self.base_position, self.updated)
        self.updated = False
