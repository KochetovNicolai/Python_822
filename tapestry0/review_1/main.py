import map_adapter
import config
import tech_bits
from UI import run_game


def main():
    print("Welcome to our strategy game!")
    print("Please, type the size of the map that you'd like to play on (x and y size)\n"
          f"x >= {config.MAP_INPUT_LIMIT['x']}, "
          f"y >= {config.MAP_INPUT_LIMIT['y']}\n"
          "Your choice: ", end="")
    map_adapter.generate_map(*tech_bits.input_map_size())
    print("Type in the number of players: ", end="")
    n = tech_bits.input_number_of_players()
    names = []
    coord = {}
    types = {}
    print(f"Choose the name, initial position x,y" +
          f"(0<=x<={config.CELL_COUNT_X - 1} и 0<=y<={config.CELL_COUNT_Y - 1})" +
          f"and types (fighter, mage, craftsman, ranger) of the players")

    for i in range(1, n + 1):
        print(f"Player №{i} name: ", end="")
        names += [str(input())]
        print(f"Initial position (x,y) of the player №{i} (on one line): ", end="")
        coord[names[-1]] = tech_bits.input_player_position()
        print(f"Type: ", end="")
        types[names[-1]] = tech_bits.input_player_type()

    run_game(names, types, coord)


if __name__ == "__main__":
    main()
