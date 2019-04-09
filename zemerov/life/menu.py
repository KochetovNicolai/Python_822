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
        if state == 'draw' and \
            field.is_inside(
                pos,
                0,
                button.Button.widht):
            return 'evolution'
        elif field.is_inside(
                pos,
                button.Button.widht,
                button.Button.widht * 2 + button.Button.margin
                ):
            return 'restart'
        elif field.is_inside(
                pos,
                button.Button.widht * 2 + button.Button.margin,
                button.Button.widht * 3 + button.Button.margin * 2
                ):
            return 'quit'
        elif field.is_inside(
                pos,
                button.Button.widht * 3 + button.Button.margin * 2,
                button.Button.widht * 4 + button.Button.margin * 3
                ):
            if state == 'evolution':
                self.prev_state = state
                return 'pause'
            elif state == 'pause':
                return 'evolution'

        return state
