import random
import time
import MyGame


class LoadTest:

    def __init__(self):
        self.loading_test()

    def test_initialization(self):
        try:
            self.count = random.randint(100000, 200000)
            player_list = [None] * self.count
            name_list = []
            for i in range(self.count):
                name_list.append(str(i))
            self.game_test = MyGame.MyGame(500, player_list, name_list)
        except BaseException:
            assert ('Initialisation doesn`t work correctly')

    def loading_test(self):
        sum = 0
        for i in range(20):
            enter_time = time.time() * 1000
            self.test_initialization()
            try:
                self.game_test.setup()
                for i in range(self.count):
                    self.game_test.fraction_choose_buttons_list[random.randint(0, 3)].on_release()
                self.game_test.start_game_program()
                for i in range(self.count):
                    self.game_test.button_list[4].on_press()
                    self.game_test.button_list[1].on_press()
                    self.game_test.update(0.012)
                self.game_test.refresh_program()
                self.game_test.next_player()
                for i in range(self.count):
                    self.game_test.place_bases(i)
                self.game_test.close()

            except BaseException:
                assert('Game doesn`t work correctly')
            out_time = time.time() * 1000
            print(i+1, end=' test works ')
            print(int(out_time - enter_time), end = ' ms\n')
            sum += int(out_time - enter_time)
        print('sum time: {} ms'.format(sum))


x = LoadTest()
