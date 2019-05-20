import Base
from UI import UI


def count_coordinates_x(x, cell_size):
    return 10 + x * cell_size - cell_size // 2


def count_coordinates_y(y, cell_size):
    return 100 + y * cell_size - cell_size // 2


class Units:
    def __init__(self):
        self.damage = 0
        self.hp = 0
        self.amount = 0
        self.unit_place = [0, 0]
        self.participated_in_turn = False
        self.defense = 1
        self.reflection = 0
        self.price = 2


class Fraction:
    def __init__(self, field_size):
        self.base = Base.Base()

        self.name = ''
        self.fraction_name = ''

        self.units = Units()

        self.unit_list = []
        self.name_units = []
        self.button_list = []
        self.name_units_text = []
        self.highlighted_cells_list = []
        self.player_list = []
        self.units_behave_list = []
        self.field_info = [[None for i in range(field_size)] for j in range(field_size)]

        self.field_size = field_size
        self.next_turn = False
        self.sound = False
        self.money = 0

        self.unit_info_x_coef = 0.6
        self.unit_info_y_coef = 0.2

        # self.unit_info = UI.Text('', self.width * self.unit_info_x_coef, self.height * self.unit_info_y_coef)

    def add_unit_button(self, x, y, cell_size, nickname, k):
        self.unit_list[k]. \
            unit_button = UI.UnitButton(x, y, count_coordinates_x(x, cell_size),
                                        count_coordinates_y(y, cell_size),
                                        self.on_push_unit_button,
                                        self.on_release_unit_button,
                                        self.unit_list[k].type,
                                        nickname, cell_size)
        self.button_list.append(self.unit_list[k].unit_button)

    def if_unit_is_dead(self, player, unit, unit_button):
        if unit.hp <= 0:
            player.unit_list.remove(unit)
            player.button_list.remove(unit_button)
            return True
        else:
            return False

    def hit_base(self, base_x, base_y, attacking_unit_x, attacking_unit_y):
        attacking_unit = None
        attacking_player = None

        base = None
        defending_player = None

        for i in self.player_list:
            for j in i.unit_list:
                if (j.unit_place[0] - 1 == attacking_unit_x) and (j.unit_place[1] - 1 == attacking_unit_y):
                    attacking_player = i
                    attacking_unit = j
                    attacking_unit.participated_in_turn = True
            if (i.base.place[0] == base_x) and (i.base.place[1] == base_y) and (not i == attacking_player):
                base = i.base
                defending_player = i

        self.highlighted_cells_list = []
        if attacking_unit is not None:
            base.hit_points -= attacking_unit.damage

        for j in self.button_list:
            if j.pressed:
                j.pressed = False

        if (base.hit_points <= 0) and (base is not None):
            self.next_turn = True
            self.player_list.remove(defending_player)

    def hit_unit(self, def_unit_x, def_unit_y, attacking_unit_x, attacking_unit_y):
        defending_unit = None
        attacking_unit = None

        defending_player = None
        attacking_player = None

        defending_unit_button = None
        attacking_unit_button = None

        for i in self.player_list:
            for j in i.unit_list:
                if (j.unit_place[0] - 1 == attacking_unit_x) and (j.unit_place[1] - 1 == attacking_unit_y):
                    attacking_player = i
                    attacking_unit = j
                    attacking_unit.participated_in_turn = True
                if (j.unit_place[0] - 1 == def_unit_x) and (j.unit_place[1] - 1 == def_unit_y):
                    defending_player = i
                    defending_unit = j
            for j in i.button_list:
                if j.pressed:
                    j.pressed = False
                if (j.x - 1 == attacking_unit_x) and (j.y - 1 == attacking_unit_y):
                    attacking_unit_button = j
                    j.pressed = False
                if (j.x - 1 == def_unit_x) and (j.y - 1 == def_unit_y):
                    defending_unit_button = j

        self.highlighted_cells_list = []
        death = False

        if defending_unit is not None:
            defending_unit.hp -= attacking_unit.damage * defending_unit.defense
        if attacking_unit is not None:
            attacking_unit.hp -= attacking_unit.damage * defending_unit.reflection

        death += self.if_unit_is_dead(attacking_player, attacking_unit, attacking_unit_button)
        death += self.if_unit_is_dead(defending_player, defending_unit, defending_unit_button)

        if death:
            return

        if attacking_unit is not None:
            attacking_unit.hp -= defending_unit.damage * attacking_unit.defense
        if defending_unit is not None:
            defending_unit.hp -= defending_unit.damage * attacking_unit.reflection

        self.if_unit_is_dead(defending_player, defending_unit, defending_unit_button)
        self.if_unit_is_dead(attacking_player, attacking_unit, attacking_unit_button)
        return

    def seek_for_empty_slot(self, x, y, add_pos, check):
        seek = False
        if (y < self.field_size) and \
           ((self.field_info[x - 1][y] is None) == check):
            add_pos.append([0, 1])
            seek = True
        if (x < self.field_size) and \
           ((self.field_info[x][y - 1] is None) == check):
            add_pos.append([1, 0])
            seek = True
        if (y > 1) and \
           ((self.field_info[x - 1][y - 2] is None) == check):
            add_pos.append([0, -1])
            seek = True
        if (x > 1) and \
           ((self.field_info[x - 2][y - 1] is None) == check):
            add_pos.append([-1, 0])
            seek = True
        return seek

    def create_unit(self, unit_type, cell_size, base_position):
        if self.money >= unit_type().price:
            # if (len(self.unit_list) == 10) and (not self.sound):
            #     sound = pygame.mixer.Sound('Easter_egg.wav')
            #     sound.play()
            #     self.sound = True
            if not self.base.destroyed:
                add_pos = []
                find = self.seek_for_empty_slot(self.base.place[0], self.base.place[1], add_pos, True)
                if find:
                    self.money -= unit_type().price
                    self.units.amount += 1
                    self.unit_list.append(unit_type())
                    self.unit_list[len(self.unit_list) - 1].participated_in_turn = True
                    self.unit_list[len(self.unit_list) - 1].unit_place[0] = base_position[0] + add_pos[0][0]
                    self.unit_list[len(self.unit_list) - 1].unit_place[1] = base_position[1] + add_pos[0][1]
                    self.add_unit_button(self.unit_list[len(self.unit_list) - 1].unit_place[0],
                                         self.unit_list[len(self.unit_list) - 1].unit_place[1],
                                         cell_size, self.name, len(self.unit_list) - 1)
        if len(self.units_behave_list) == 0:
            self.next_turn = True

    def on_push_highlighted_cell(self, x, y, unit_x, unit_y, nickname, cell_size):
        # self.unit_info = UI.Text('', self.height * self.unit_info_y_coef, self.width * self.unit_info_x_coef)
        for k, i in enumerate(self.unit_list):
            if (i.unit_place[0] == unit_x + 1) and (i.unit_place[1] == unit_y + 1):
                i.unit_place[0] = x + 1
                i.unit_place[1] = y + 1
                self.units_behave_list.remove(i)
                i.participated_in_turn = True
                self.add_unit_button(i.unit_place[0], i.unit_place[1], cell_size, nickname, k)
        for i in range(len(self.button_list) - 1):
            if (self.button_list[i].x == unit_x + 1) and (self.button_list[i].y == unit_y + 1):
                self.button_list.remove(self.button_list[i])
                self.highlighted_cells_list = []
        if len(self.units_behave_list) == 0:
            self.next_turn = True

    def on_release_unit_button(self):
        # self.unit_info = UI.Text('', self.height * self.unit_info_y_coef, self.width * self.unit_info_x_coef)
        self.highlighted_cells_list = []

    def depress_buttons(self):
        for i in self.player_list:
            for j in i.button_list:
                if j.pressed:
                    j.pressed = False

    def find_unit(self, x, y):
        unit_now = None
        for i in self.unit_list:
            if [x, y] == [i.unit_place[0], i.unit_place[1]]:
                # self.unit_info = UI.Text('жизни: {}, урон: {}, тип: {}'.format(i.hp, i.damage, i.type),
                #                          self.height * self.unit_info_y_coef, self.width * self.unit_info_x_coef)
                unit_now = i
        return unit_now

    def create_highlighted_cell_button(self, x, y, i, function_to_do, cell_size, nickname, action_type, delta=0):
        return UI.HighlightedCellButton(count_coordinates_x(x + i[0], cell_size),
                                        count_coordinates_y(y + i[1], cell_size),
                                        function_to_do, '',
                                        nickname, x + i[0] - delta, y + i[1] - delta,
                                        x - 1, y - 1,
                                        cell_size, action_type)

    def on_move(self, add_highlighted_cells, x, y, cell_size, nickname):
        for i in add_highlighted_cells:
            self.highlighted_cells_list.append(self.create_highlighted_cell_button(x, y, i,
                                                                                   self.on_push_highlighted_cell,
                                                                                   cell_size, nickname, 'move', 1))

    def on_attack(self, add_highlighted_attack_cells, x, y, cell_size, nickname):
        for i in add_highlighted_attack_cells:
            friendly_fire = False
            base_attack = False

            for j in self.unit_list:
                if (j.unit_place[0] == x + i[0]) and (j.unit_place[1] == y + i[1]):
                    friendly_fire = True

            for j in self.player_list:
                if (j.base.place[0] == x + i[0]) and (j.base.place[1] == y + i[1]):
                    base_attack = True

            if (not friendly_fire) and (not base_attack):
                self.highlighted_cells_list.append(self.create_highlighted_cell_button(x, y, i,
                                                                                       self.hit_unit,
                                                                                       cell_size, nickname, 'attack', 1))

            if base_attack and (not (self.base.place[0] == x + i[0] and (self.base.place[1] == y + i[1]))):
                self.highlighted_cells_list.append(self.create_highlighted_cell_button(x, y, i,
                                                                                       self.hit_base,
                                                                                       cell_size, nickname,
                                                                                       'attack_base'))

    def on_push_unit_button(self, x, y, cell_size, nickname):
        self.depress_buttons()

        unit_now = self.find_unit(x, y)

        if not unit_now.participated_in_turn:
            self.highlighted_cells_list = []
            add_highlighted_cells = []
            find = self.seek_for_empty_slot(x, y, add_highlighted_cells, True)
            if find:
                self.on_move(add_highlighted_cells, x, y, cell_size, nickname)

            add_highlighted_attack_cells = []
            find_sth_to_attack = self.seek_for_empty_slot(x, y, add_highlighted_attack_cells, False)
            if find_sth_to_attack:
                self.on_attack(add_highlighted_attack_cells, x, y, cell_size, nickname)

    def count_units(self, text):
        print('{} имеют {} юнитов'.format(text, self.units.amount))

    def info_about_units(self, text):
        s = 'Информация о \nюнитах игрока {}:\n'.format(self.name)
        s += 'Фракция: {}\n'.format(text)
        for i in self.unit_list:
            s += 'Юнит: {}, урон: {}, хп: {}, клетка: {}\n'.format(i.type, i.damage, i.hp, i.unit_place)
        s += 'Местоположение базы: {}, хп: {}\n'.format(self.base.place, self.base.hit_points)
        s += '{} имеют {} юнитов\n'.format(text, self.units.amount)
        s += 'Всего денег {}'.format(self.money)
        return s


class CriminalFraction(Fraction):
    def __init__(self, field_size):
        super().__init__(field_size)
        self.name_units.append(Bydlan)
        self.name_units.append(Bariga)
        self.name_units.append(Offnik)
        self.name_units.append(Zek)
        self.name_units_text.append(Bydlan().type)
        self.name_units_text.append(Bariga().type)
        self.name_units_text.append(Offnik().type)
        self.name_units_text.append(Zek().type)
        self.fraction_name = 'Преступники'

    def info_about_units(self):
        return super().info_about_units("Преступники")

    def count_units(self):
        super().count_units("Преступники")


class Bydlan(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Быдлан'


class Bariga(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 3
        self.type = 'Барыга'


class Offnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 5
        self.type = 'Оффник'


class Zek(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 7
        self.type = 'Зэк'


###############################################################NEXTFRACTION###############
class MajorsFraction(Fraction):
    def __init__(self, field_size):
        super().__init__(field_size)
        self.name_units.append(Podsosnik)
        self.name_units.append(Pokazushnik)
        self.name_units.append(Major)
        self.name_units.append(MainMajor)
        self.name_units_text.append(Podsosnik().type)
        self.name_units_text.append(Pokazushnik().type)
        self.name_units_text.append(Major().type)
        self.name_units_text.append(MainMajor().type)
        self.fraction_name = 'Мажоры'

    def count_units(self):
        super().count_units('Мажоры')

    def info_about_units(self):
        return super().info_about_units("Мажоры")


class Podsosnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.hp = 2
        self.type = 'Подсосник'


class Pokazushnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Показушник'


class Major(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 4
        self.type = 'Мажор'


class MainMajor(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 6
        self.type = 'Мажорище'


###############################################################NEXTFRACTION###############
class PartyFraction(Fraction):
    def __init__(self, field_size):
        super().__init__(field_size)
        self.name_units.append(Fan)
        self.name_units.append(Modnik)
        self.name_units.append(Strelocnik)
        self.name_units.append(Misha)
        self.name_units_text.append(Fan().type)
        self.name_units_text.append(Modnik().type)
        self.name_units_text.append(Strelocnik().type)
        self.name_units_text.append(Misha().type)
        self.fraction_name = 'Тусовщики'

    def count_units(self):
        super().count_units("Тусовщики")

    def info_about_units(self):
        return super().info_about_units("Тусовщики")


class Fan(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 1
        self.type = 'Фанатка'


class Modnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Модник'


class Strelocnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 4
        self.type = 'Стрелочник'


class Misha(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 9
        self.type = 'Миша'


###############################################################NEXTFRACTION###############
class BotansFraction(Fraction):
    def __init__(self, field_size):
        super().__init__(field_size)
        self.name_units.append(Dohodyaga)
        self.name_units.append(Otlychnik)
        self.name_units.append(Tupoydrug)
        self.name_units.append(Lubimchik)
        self.name_units_text.append(Dohodyaga().type)
        self.name_units_text.append(Otlychnik().type)
        self.name_units_text.append(Tupoydrug().type)
        self.name_units_text.append(Lubimchik().type)
        self.fraction_name = 'Ботаны'

    def count_units(self):
        super().count_units("Ботаны")

    def info_about_units(self):
        return super().info_about_units("Ботаны")


class Dohodyaga(Units):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.hp = 1
        self.type = 'Доходяга'


class Otlychnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Отличник'


class Tupoydrug(Units):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.hp = 12
        self.type = 'Тупой друг'


class Lubimchik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 4
        self.hp = 1
        self.type = 'Любимчик'
