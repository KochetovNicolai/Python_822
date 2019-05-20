import unittest
import random
import Base
import MyGame
from Fractions import CriminalFraction, BotansFraction, MajorsFraction, PartyFraction


class UnitTest(unittest.TestCase):

    def test_initialization(self):
        try:
            self.count = random.randint(1, 5)
            player_list = [None] * self.count
            name_list = []
            for i in range(self.count):
                name_list.append(str(i))
            self.game_test = MyGame.MyGame(10, player_list, name_list)
        except BaseException:
            self.assertTrue(False, 'Initialisation doesn`t work correctly')

    def test_base(self):
        temp = Base.Base()
        self.assertEqual(type(temp), Base.Base, 'Base doesn`t work correctly')
        self.assertTrue(temp.hit_points == 10, 'Base doesn`t work correctly')
        self.assertTrue(temp.place == [0, 0], 'Base doesn`t work correctly')
        self.assertFalse(temp.destroyed, 'Base doesn`t work correctly')
        self.assertTrue(temp.type == 'Base', 'Base doesn`t work correctly')

    def test_game_update(self):
        self.test_initialization()
        try:
            self.game_test.setup()
            for i in range(self.count):
                self.game_test.fraction_choose_buttons_list[random.randint(0, 3)].on_release()
            self.game_test.start_game_program()
            self.game_test.update(0.012)
            self.game_test.refresh_program()
            self.game_test.next_player()
            for i in range(self.count):
                self.game_test.place_bases(i)
            self.game_test.close()
        except BaseException:
            self.assertTrue(False, 'Game doesn`t work correctly')

    def test_units(self):
        frac_list = [CriminalFraction.CriminalFraction,
                     MajorsFraction.MajorsFraction,
                     PartyFraction.PartyFraction,
                     BotansFraction.BotansFraction]
        for i in range(4):
            n = random.randint(0, 3)
            temporary = frac_list[n](10, 800, 600)
            cell_size = 45
            temporary.money += 20
            for j in range(0, 3):
                unit = random.randint(0, 3)
                temporary.create_unit(temporary.name_units[unit], cell_size, temporary.base.place)
                self.assertEqual(temporary.unit_list[j].type, temporary.name_units[unit]().type)
                self.assertEqual(len(temporary.unit_list), j+1)


if __name__ == '__main__':
    unittest.main()
