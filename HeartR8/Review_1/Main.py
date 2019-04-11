import MyGame
import arcade


def main():
    field_size = 10
    print('Enter number of players:')
    number_of_players = int(input())
    player_list = [None] * number_of_players
    name_list = []
    for i in range(len(player_list)):
        print('Player {}'.format(i + 1))
        print('Give name to your fraction:')
        name_list.append(input())
    game = MyGame.MyGame(1200, 650, field_size, player_list, name_list)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
