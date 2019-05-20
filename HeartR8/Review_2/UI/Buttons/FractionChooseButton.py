from UI.Buttons.TextButton import TextButton


class FractionChooseButton(TextButton):
    def __init__(self, center_x, center_y, action_function, fraction, text):
        super().__init__(center_x, center_y, 140, 40, text, 18, "Arial")
        self.action_function = action_function
        self.fraction = fraction

    def on_release(self):
        super().on_release()
        self.action_function(self.fraction)
