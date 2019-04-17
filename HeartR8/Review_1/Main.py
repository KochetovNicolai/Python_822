import MyGame
import arcade


def main():
    print('Enter number of players:')
    entered = False
    number_of_players = 0

    while not entered:
        try:
            number_of_players = int(input())
            entered = True
        except ValueError:
            print("Enter numbers, not letters")
            entered = False

    player_list = [None] * number_of_players
    name_list = []
    for i in range(len(player_list)):
        print('Player {}'.format(i + 1))
        print('Give name to your fraction:')
        name = input()
        name_entered = False

        while not name_entered:
            try:
                name_list.index(name)
                print('This fraction name is already taken')
                name = input()
            except ValueError:
                name_entered = True
                name_list.append(name)

    field_size = 10

    game = MyGame.MyGame(field_size, player_list, name_list)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
