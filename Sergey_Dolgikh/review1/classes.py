import vars, functions


class Button:
    count = 0 # кол-во предметов
    button_vertical_align = 35
    button_horizontal_align = 20
    hint_vertical_align = 33
    hint_horizontal_align = 15

    def __init__(self, name, multiple_name, cost, production):
        self.multiple_name = multiple_name
        self.name = name
        self.cost = cost
        self.prod = production

    def draw(self, coords):
        if self.cost <= vars.accumulative.cookies:
            self.buy_rec = functions.button_rectangle(vars.screen, vars.fontObj1, 'Buy {} for {} cookies'.format(self.name, round(self.cost, 2)),
                                                      vars.black, vars.grey, coords, 1)
        else:
            self.buy_rec = functions.button_rectangle(vars.screen, vars.fontObj1, 'Buy {} for {} cookies'.format(self.name, round(self.cost, 2)),
                                                      vars.grey, vars.light_grey, coords, 1)
        if functions.has_enough_money(10, self.cost, vars.accumulative.cookies):
            self.buy10_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'x10', vars.black, vars.grey,
                                                         (coords[0] - self.button_horizontal_align, coords[1] + self.button_vertical_align), 1)
        else:
            self.buy10_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'x10', vars.grey, vars.light_grey,
                                                         (coords[0] - self.button_horizontal_align, coords[1] + self.button_vertical_align), 1)
        if self.cost <= vars.accumulative.cookies:
            self.buymax_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'Max', vars.black, vars.grey,
                                                          (coords[0] + self.button_horizontal_align, coords[1] + self.button_vertical_align), 1)
        else:
            self.buymax_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'Max', vars.grey, vars.light_grey,
                                                          (coords[0] + self.button_horizontal_align, coords[1] + self.button_vertical_align), 1)

class ButtonPerSec(Button):
    def buy(self, n):
        if functions.has_enough_money(n, self.cost, vars.accumulative.cookies):
            for i in range(n):
                vars.accumulative.cookies -= self.cost
                vars.accumulative.cookies_income += self.prod
                self.count += 1
                self.cost *= 1.1

    def on_point(self, pos):
        functions.button_rectangle(vars.screen, vars.fontObj2, 'You have {} of {}'.format(self.count, self.multiple_name), vars.black,
                                   vars.white, (pos[0], pos[1] + self.hint_horizontal_align), 0)
        functions.button_rectangle(vars.screen, vars.fontObj2, ' Each produces {} cookies per second'.format(self.prod), vars.black,
                                   vars.white, (pos[0], pos[1] + self.hint_vertical_align), 0)

class ButtonPerClick(Button):
    def buy(self, n):
        if functions.has_enough_money(n, self.cost, vars.accumulative.cookies):
            for i in range(n):
                vars.accumulative.cookies -= self.cost
                vars.accumulative.cookies_per_click += self.prod
                self.count += 1
                self.cost *= 1.1

    def on_point(self, pos):
        functions.button_rectangle(vars.screen, vars.fontObj2, 'You have {} of {}'.format(self.count, self.multiple_name), vars.black,
                                   vars.white, (pos[0], pos[1] + self.hint_horizontal_align), 0)
        functions.button_rectangle(vars.screen, vars.fontObj2, ' Each produces {} of cookies per click'.format(self.prod), vars.black,
                                   vars.white, (pos[0], pos[1] + self.hint_vertical_align), 0)

oven = ButtonPerSec('an oven', 'ovens', 10, 1)
farm = ButtonPerSec('a cookie farm', 'cookie farms', 1000, 50)
factory = ButtonPerSec('a cookie factory', 'cookie factories', 100000, 2500)
extra_hand = ButtonPerClick('extra hand', 'extra hands', 10, 1)
manipulator = ButtonPerClick('manipulator', 'manipulators', 1000, 50)
robot = ButtonPerClick('robot', 'robots', 100000, 2500)
items = [oven, farm, factory, extra_hand, manipulator, robot]
