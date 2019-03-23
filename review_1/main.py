import arcade
from unit import Unit
from event import Event, EventId
import UI
from action import Bolt


class MyGame(arcade.Window):

    def __init__(self, names, coordinates):
        super().__init__(UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)

        arcade.set_background_color(arcade.color.AMAZON)

        self.names = names
        self.coordinates = coordinates
        self.events = None
        self.names_mapping = {}
        self.player_list = None
        self.action_list = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.action_list = arcade.SpriteList()

        for name in self.names:
            self.names_mapping[name] = Unit(self.coordinates[name][0] + UI.SCREEN_DELTA,
                                            self.coordinates[name][1] + UI.SCREEN_DELTA,
                                            "mage.png", name)  # заглушка - UI.SCREEN_DELTA

            self.player_list.append(self.names_mapping[name])

        self.events = Event(self.names_mapping.values())

    def on_draw(self):
        arcade.start_render()
        UI.draw_map()
        if self.events.game_over():
            winner = self.events.get_current_player()
            for name, temp in self.names_mapping.items():
                if temp == winner:
                    winner = name
                    break
            UI.you_win(winner)
        else:
            self.player_list.draw()
            for unit in self.player_list:
                unit.draw()

            self.action_list.draw()
            for unit_a in self.action_list:
                unit_a.draw()

            UI.display_turn(self.events.get_current_player())
            # for i in range(len(self.names)):
            #    name = self.names[i]
            #    output = f"{name}\nhp : {self.names_mapping[name].hp}"
            #    UI.display_unit_stats(output, number_of_units=len(self.names), unit=i + 1)

    def hit_unit(self, unit, attack):
        if unit == self.events.get_current_player():
            pass

        unit.hp -= attack.damage
        if unit.hp <= 0:
            unit.kill()
            self.events.kill_unit(unit)

    def update(self, delta_time):
        self.player_list.update()
        self.action_list.update()

        for action in self.action_list:
            hit_list = arcade.check_for_collision_with_list(action, self.player_list)
            if len(hit_list) > 0:
                action.kill()
            for unit in hit_list:
                self.hit_unit(unit, action)

    def on_key_press(self, key, modifiers):
        event_id, sprite = self.events.get_event()

        if key in UI.MOVE_KEYS:
            if event_id == EventId.MOVE_EVENT:
                sprite.make_move(key)
            else:
                pass

        if key == UI.NEXT_TURN_KEY:
            self.events.pop_event()
            self.events.next_unit_turn()
            sprite.turn_pos_update(sprite.center_x, sprite.center_y)

    def on_key_release(self, key, modifiers):
        event_id, sprite = self.events.get_event()

        if event_id == EventId.MOVE_EVENT:
            if key in UI.MOVE_KEYS:
                sprite.stop_move(key)

    def on_mouse_press(self, x, y, button, modifiers):
        _, sprite = self.events.get_event()

        if button == arcade.MOUSE_BUTTON_LEFT:
            x = x - sprite.center_x
            y = y - sprite.center_y
            c = (x ** 2 + y ** 2) ** 0.5
            self.action_list.append(
                Bolt(sprite.center_x + UI.ACTION_DELTA * x / c, sprite.center_y + UI.ACTION_DELTA * y / c, 10 * x / c,
                     10 * y / c,
                     "fireball.png"))
            self.events.action_count -= 1
            if self.events.action_count == 0:
                self.events.pop_event()
                self.events.next_unit_turn()
                sprite.turn_pos_update(sprite.center_x, sprite.center_y)



def main():
    print("Введите количество игроков: ", end="")
    N = int(input())
    names = []
    coord = {}
    print(f"Введите имена и координаты x,y (0<=x<={UI.screen_width()} и 0<=y<={UI.screen_height()}) игроков")
    for i in range(1, N + 1):
        print(f"Имя игрока №{i}: ", end="")
        names += [str(input())]
        print(f"Начальные координаты (x,y) игрока №{i} на одной строке: ", end="")
        coord[names[len(names) - 1]] = tuple(map(int, input().split()))

    game = MyGame(names, coord)
    game.setup()
    arcade.run()
    arcade.window_commands.close_window()


if __name__ == "__main__":
    main()
