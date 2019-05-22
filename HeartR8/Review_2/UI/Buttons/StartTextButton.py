from UI.Buttons.TextButton import TextButton


class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function, text, size_x=180, size_y=40):
        super().__init__(center_x, center_y, size_x, size_y, text, 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()
