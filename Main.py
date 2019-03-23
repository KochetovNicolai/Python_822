import MyGame
import arcade


def main():
    print('Fractions:\n'
          '1) Criminals\n'
          '2) Majors\n'
          '3) Party-goers\n'
          '4) Nerds\n')
    print('Enter number of players:')
    player_list = []
    frac_list = [MyGame.Game_classes.CriminalFraction,
                 MyGame.Game_classes.MajorsFraction,
                 MyGame.Game_classes.PartyFraction,
                 MyGame.Game_classes.BotansFraction]
    for i in range(1, int(input()) + 1):
        print('Player {}'.format(i))
        print('Choose your fraction:\n'
              '(type number of chosen fraction)')
        frac_num = int(input()) - 1
        player_list.append(frac_list[frac_num]())
    game = MyGame.MyGame(1200, 650, 10, player_list)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
