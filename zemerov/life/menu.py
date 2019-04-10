import field
import button


class Menu:
    """В Menu опишем 4 кнопки start, restart, quit, pause"""

    FONT = 'calibri'
    FONT_SIZE = 36

    def __init__(self, game_f):
        self.prev_state = 'draw'

        self.start = button.Button(
            'start',
            Menu.FONT,
            Menu.FONT_SIZE,
            0,
            game_f.field_size[1] - field.Field.menu_height
        )

        self.restart = button.Button(
            'restart',
            Menu.FONT,
            Menu.FONT_SIZE,
            button.Button.widht + button.Button.margin,
            game_f.field_size[1] - field.Field.menu_height
        )

        self.quit = button.Button(
            'quit',
            Menu.FONT,
            Menu.FONT_SIZE,
            (button.Button.widht + button.Button.margin) * 2,
            game_f.field_size[1] - field.Field.menu_height
        )

        self.pause = button.Button(
            'pause',
            Menu.FONT,
            Menu.FONT_SIZE,
            (button.Button.widht + button.Button.margin) * 3,
            game_f.field_size[1] - field.Field.menu_height
        )

    def draw(self, surface):
        for but in (self.start, self.restart, self.quit, self.pause):
            but.draw(surface)

    def click(self, pos, state):
        if state == 'draw' and self.start.is_inside(pos):
            return 'evolution'
        elif self.restart.is_inside(pos):
            return 'restart'
        elif self.quit.is_inside(pos):
            return 'quit'
        elif self.pause.is_inside(pos):
            if state == 'evolution':
                self.prev_state = state
                return 'pause'
            elif state == 'pause':
                return 'evolution'

        return state
