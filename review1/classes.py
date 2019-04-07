import vars, functions


class Button:
    count = 0 # кол-во предметов

    def __init__(self, name, multiple_name, cost, production):
        self.multiple_name = multiple_name
        self.name = name
        self.cost = cost
        self.prod = production

    def draw(self, coords):
        if self.cost <= vars.cookies:
            self.buy_rec = functions.button_rectangle(vars.screen, vars.fontObj1, 'Buy {} for {} cookies'.format(self.name, round(self.cost, 2)),
                                                      vars.black, vars.grey, coords, 1)
        else:
            self.buy_rec = functions.button_rectangle(vars.screen, vars.fontObj1, 'Buy {} for {} cookies'.format(self.name, round(self.cost, 2)),
                                                      vars.grey, vars.light_grey, coords, 1)
        if functions.strange_formula(10,self.cost, vars.cookies):
            self.buy10_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'x10', vars.black, vars.grey, (coords[0] - 20, coords[1] + 35), 1)
        else:
            self.buy10_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'x10', vars.grey, vars.light_grey, (coords[0] - 20, coords[1] + 35), 1)
        if self.cost <= vars.cookies:
            self.buymax_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'Max', vars.black, vars.grey, (coords[0] + 20, coords[1] + 35), 1)
        else:
            self.buymax_rect = functions.button_rectangle(vars.screen, vars.fontObj1, 'Max', vars.grey, vars.light_grey, (coords[0] + 20, coords[1] + 35), 1)

class Button_per_sec(Button):
    def buy(self, n):
        if functions.strange_formula(n, self.cost, vars.cookies):
            for i in range(n):
                vars.cookies -= self.cost
                vars.cookies_income += self.prod
                self.count += 1
                self.cost *= 1.1

    def is_pointed(self, pos):
        functions.button_rectangle(vars.screen, vars.fontObj2, 'You have {} of {}'.format(self.count, self.multiple_name), vars.black,
                                   vars.white, (pos[0], pos[1] + 15), 0)
        functions.button_rectangle(vars.screen, vars.fontObj2, ' Each produces {} cookies per second'.format(self.prod), vars.black,
                                   vars.white, (pos[0], pos[1] + 33), 0)

class Button_per_click(Button):
    def buy(self, n):
        if functions.strange_formula(n, self.cost, vars.cookies):
            for i in range(n):
                vars.cookies -= self.cost
                vars.cookies_per_click += self.prod
                self.count += 1
                self.cost *= 1.1

    def is_pointed(self, pos):
        functions.button_rectangle(vars.screen, vars.fontObj2, 'You have {} of {}'.format(self.count, self.multiple_name), vars.black,
                                   vars.white, (pos[0], pos[1] + 15), 0)
        functions.button_rectangle(vars.screen, vars.fontObj2, ' Each produces {} of cookies per click'.format(self.prod), vars.black,
                                   vars.white, (pos[0], pos[1] + 33), 0)

oven = Button_per_sec('an oven', 'ovens', 10, 1)
farm = Button_per_sec('a cookie farm', 'cookie farms', 1000, 50)
factory = Button_per_sec('a cookie factory', 'cookie factories', 100000, 2500)
extra_hand = Button_per_click('extra hand', 'extra hands', 10, 1)
manipulator = Button_per_click('manipulator', 'manipulators', 1000, 50)
robot = Button_per_click('robot', 'robots', 100000, 2500)
items = [oven, farm, factory, extra_hand, manipulator, robot]