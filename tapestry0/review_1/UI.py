from arcade import draw_commands, draw_text, color
import arcade
import game_manager
import map_adapter
import mapping
from classes import Unit
import config


def draw_background():
    map_texture = draw_commands.load_texture(config.MAP_BACKGROUND)
    draw_commands.draw_texture_rectangle(center_x=config.SCREEN_WIDTH / 2,
                                         center_y=config.SCREEN_HEIGHT / 2,
                                         width=config.SCREEN_WIDTH,
                                         height=config.SCREEN_HEIGHT, texture=map_texture)


def you_win(winner):
    x = 0
    y = 0
    draw_text(f"{winner.upper()} WINS!!!", x, y, color.WHITE,
              font_size=120 * (config.CELL_COUNT_X * config.CELL_COUNT_Y / (25 * 15)))


def game_over():
    if game_manager.Game().winner() is not None:
        winner = game_manager.Game().winner()
        you_win(winner)
        return True
    else:
        return False


def display_cell_state(cell):
    if isinstance(cell, map_adapter.Cell):
        if cell is None:
            pass
        elif cell.state is None:
            mapping.display_height(cell)
        else:
            if isinstance(cell.state, Unit):
                stats = cell.state.stats
                output_stats = f"hp: {round(stats.hp, 2)}\nspeed: {stats.speed}\ndamage:" + \
                               f" {stats.damage}\nitems:" + \
                               f" {stats.items}\nvision: {stats.vision}"
                arcade.text.draw_text(text=output_stats, start_x=0,
                                      start_y=config.SCREEN_HEIGHT,
                                      color=arcade.color.GOLD,
                                      font_size=20)

                states = cell.state.states
                output_states = "active"
                if not states.participates:
                    output_states = "inactive"
                arcade.text.draw_text(text=output_states, start_x=0,
                                      start_y=config.SCREEN_HEIGHT + config.UPPER_GAP - 20,
                                      color=arcade.color.GOLD,
                                      font_size=20)


def display_current_turn():
    current = game_manager.current_turn()
    arcade.text.draw_text(f"{current.name}'s\nturn", config.SCREEN_WIDTH + config.RIGHT_GAP / 10,
                          config.SCREEN_HEIGHT + config.UPPER_GAP / 10,
                          arcade.color.GOLD, 50)

    activity = current.activity
    output_activity = f"{current}\nsteps left: {activity.steps}\nactions left: {activity.actions}"
    arcade.text.draw_text(text=output_activity, start_x=config.SCREEN_WIDTH,
                          start_y=0,
                          color=arcade.color.GOLD,
                          font_size=20)

    for cell in mapping.nearby_cells(current.cell):
        mapping.display_height(cell)


def _check_current_move(key):
    if key in config.MOVE_KEYS:
        game_manager.move_current(get_direction(key))


def _check_next_turn(key):
    if key == config.NEXT_TURN_KEY:
        game_manager.next_turn()


def get_direction(key):
    if key in config.MOVE_KEYS:
        return config.MOVE_DIRECTION[key]
    else:
        raise Exception


class MyGame(arcade.Window):
    def __init__(self):
        true_width = config.SCREEN_WIDTH + config.RIGHT_GAP
        true_height = config.SCREEN_HEIGHT + config.UPPER_GAP
        super().__init__(true_width, true_height)

        self.player_sprites = None
        self.attack_sprites = None
        self.aura_sprites = None
        self.player_list = None
        self.attack_list = None
        self.aura_list = None
        self.inspected_cell = None

    def _draw_objects(self):
        self.player_sprites.draw()
        for sprite in self.player_sprites:
            sprite.draw()

        self.attack_sprites.draw()
        for sprite in self.attack_sprites:
            sprite.draw()

        self.aura_sprites.draw()
        for sprite in self.aura_sprites:
            sprite.draw()

    def _update_objects(self):
        self.player_sprites.update()
        self.attack_sprites.update()
        self.aura_sprites.update()
        for unit in self.player_list:
            unit.update()
        for action in self.attack_list:
            action.update()
        for aura in self.aura_list:
            # print(aura.exists())
            aura.update()

    def _set_initial_units(self):
        for unit in game_manager.Game().names_mapping.values():
            self.player_list.append(unit)
            self.player_sprites.append(game_manager.object_to_sprite(unit))

    def _perform_action_hits(self):
        for action in self.attack_sprites:
            hit_list = arcade.check_for_collision_with_list(action, self.player_sprites)
            if len(hit_list) > 0:
                game_manager.kill_action(game_manager.sprite_to_object(action))
            for unit in hit_list:
                game_manager.hit_actor(game_manager.sprite_to_object(unit),
                                       game_manager.sprite_to_object(action))

    def _check_create_current_attack(self, button, cell):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.attack_list.append(game_manager.create_current_attack(cell))
            self.attack_sprites.append(game_manager.object_to_sprite(self.attack_list[-1]))

    def _check_create_current_aura(self, button, cell):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.aura_list.append(game_manager.create_current_aura_over(cell))
            self.aura_sprites.append(game_manager.object_to_sprite(self.aura_list[-1]))

    def _cell_inspection(self):
        if self.inspected_cell is not None:
            display_cell_state(self.inspected_cell)

    def _cell_highlight(self):
        if self.inspected_cell is not None:
            current = game_manager.current_turn()
            if 1 < mapping.cab_distance(mapping.get_cell(current), self.inspected_cell)\
                    <= current.stats.vision:
                mapping.highlight(self.inspected_cell, _color=arcade.color.RED)
            else:
                mapping.highlight(self.inspected_cell)

    def setup(self):
        self.player_sprites = arcade.SpriteList()
        self.attack_sprites = arcade.SpriteList()
        self.aura_sprites = arcade.SpriteList()
        self.player_list = []
        self.attack_list = []
        self.aura_list = []
        self._set_initial_units()

    def on_draw(self):
        arcade.start_render()
        draw_background()
        if game_over():
            pass
        else:
            display_current_turn()
            self._cell_highlight()
            self._cell_inspection()
            self._draw_objects()

    def update(self, delta_time):
        game_manager.update()
        self._update_objects()
        self._perform_action_hits()

    def on_key_press(self, key, modifiers):
        _check_current_move(key)
        _check_next_turn(key)

    def on_key_release(self, key, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        cell = mapping.raw_to_cell(x, y)
        if cell is not None:
            self._check_create_current_attack(button, cell)
            self._check_create_current_aura(button, cell)

    def on_mouse_motion(self, x, y, dx, dy):
        self.inspected_cell = mapping.raw_to_cell(x, y)


def run_game(names, unit_classes, coordinates):
    game_manager.setup(names, unit_classes, coordinates)
    game = MyGame()
    game.setup()
    arcade.run()
    arcade.window_commands.close_window()
