# to be done:
# 1)sometimes when the mouse cursor goes out of the window (along the border),
#   cells get processed in main.MyGame's on_mouse method - will be taken care of in later releases
# 2)sprite collision algorithm sometimes sees the collision between the attack and the attacker sprites
#   in the moment of attacking, immediately discarding the attack's sprite and hitting the attacker,
#   which is not displayed to the user and is just absurd, but i haven't found a way yet to solve the issue,
#   which is why, for the time being, attack cannot be directed to the nearest 4 cells
# 3)separate module for user interface management
#   self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE1(2) are temporary variables to enable cell highlighting
#    (one in the attack range, another over the rest of the map)
#   self.show is a function object to display unit's stats when the mouse pointer is right over it


import arcade
import UI
import mapping
import event_manager
import object_manager


class MyGame(arcade.Window):

    def __init__(self, names, types, coordinates):
        super().__init__(UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)

        arcade.set_background_color(arcade.color.AMAZON)

        self.names = names
        self.types = types
        self.coordinates = coordinates
        self.events = None
        self.names_mapping = {}
        self.player_list = None
        self.action_list = None
        self.show = None

        self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE1 = None
        self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE2 = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.action_list = arcade.SpriteList()

        for name in self.names:
            x, y = self.coordinates[name]
            self.names_mapping[name] = event_manager.create_unit(x, y, name, self.types[name])

            self.player_list.append(self.names_mapping[name])

        event_manager.initialise()

    def on_draw(self):
        arcade.start_render()
        mapping.draw_background()
        if event_manager.winner() is not None:
            winner = event_manager.winner()
            for name, temp in self.names_mapping.items():
                if temp == winner:
                    winner = name
                    break
            UI.you_win(winner)
        else:
            # vision highlight (attack distance, etc.) - will later be implemented in a more neat way
            if self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE1 is not None:
                mapping.highlight(self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE1, _color=arcade.color.RED)
            elif self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE2 is not None:
                mapping.highlight(self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE2)

            if self.show is not None:
                self.show()
            self.player_list.draw()
            for unit in self.player_list:
                unit.draw()

            self.action_list.draw()
            for unit_a in self.action_list:
                unit_a.draw()

    def update(self, delta_time):
        event_manager.update()
        self.player_list.update()
        self.action_list.update()

        for action in self.action_list:
            hit_list = arcade.check_for_collision_with_list(action, self.player_list)
            if len(hit_list) > 0:
                action.kill()
            for unit in hit_list:
                event_manager.hit_actor(unit, action)

    def on_key_press(self, key, modifiers):
        sprite = event_manager.current_turn()

        if key in UI.MOVE_KEYS:
            event_manager.move(sprite, key)

        if key == UI.NEXT_TURN_KEY:
            event_manager.next_turn()

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        sprite = event_manager.current_turn()

        cell = mapping.raw_to_cell(x, y)
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.action_list.append(event_manager.create_attack(sprite, cell))

    def on_mouse_motion(self, x, y, dx, dy):
        cell = mapping.raw_to_cell(x, y)

        sprite = event_manager.current_turn()
        if mapping.cab_distance(mapping.get_cell(sprite), cell) <= sprite.stats.vision and mapping.cab_distance(
                mapping.get_cell(sprite), cell) > 1:
            self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE1 = cell
            self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE2 = None
        else:
            self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE1 = None
            self.HIGHLIGHT_TO_BE_CHANGED_AT_RELEASE2 = cell

        self.show = object_manager.display_state_func(cell)  # func as object


def main():
    print("Type in the number of players: ", end="")
    n = UI.input_number_of_players()
    names = []
    coord = {}
    types = {}
    print(
        f"Choose the name, initial position x,y (0<=x<={UI.CELL_COUNT_X - 1} и 0<=y<={UI.CELL_COUNT_Y - 1}) and types (fighter, mage, craftsman, ranger) of the players")

    for i in range(1, n + 1):
        print(f"Player №{i} name: ", end="")
        names += [str(input())]
        print(f"Initial position (x,y) of the player №{i} (on one line): ", end="")
        coord[names[-1]] = UI.input_player_position()
        print(f"Type: ", end="")
        types[names[-1]] = UI.input_player_type()

    game = MyGame(names, types, coord)
    game.setup()
    arcade.run()
    arcade.window_commands.close_window()


if __name__ == "__main__":
    main()
