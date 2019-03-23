import Base
import UI


class Units:
    def __init__(self):
        self.damage = 0
        self.hp = 0
        self.amount = 0
        self.unit_place = [0, 0]


class Fraction:
    def __init__(self):
        self.base = Base.Base()
        print('Give name to your fraction:')
        self.name = input()
        print('Base of {} is created, hit points: {}'.format(self.name, self.base.hit_points))
        self.units = Units()
        self.unit_list = []
        self.name_units = []
        self.button_list = []
        self.highlighted_cells_list = []

    def unit_button(self, x, y, cell_size, nickname):
        self.unit_list[len(self.unit_list) - 1]. \
            unit_button = UI.UnitButton(10 + x * cell_size - cell_size // 2,
                                        100 + y * cell_size - cell_size // 2,
                                        self.push_unit_button,
                                        self.unit_list[len(self.unit_list) - 1].type,
                                        nickname, cell_size)
        self.button_list.append(self.unit_list[len(self.unit_list) - 1].unit_button)

    def create_unit(self, unit_type, cell_size):
        self.units.amount += 1
        self.unit_list.append(unit_type())
        if self.base.place != [-100, -100]:
            if self.base.place[1] < 10:
                self.unit_list[len(self.unit_list) - 1].unit_place[0] = self.base.place[0]
                self.unit_list[len(self.unit_list) - 1].unit_place[1] += self.base.place[1] + 1
                self.unit_button(self.unit_list[len(self.unit_list) - 1].unit_place[0],
                                 self.unit_list[len(self.unit_list) - 1].unit_place[1],
                                 cell_size, self.name)
            elif self.base.place[0] < 10:
                self.unit_list[len(self.unit_list) - 1].unit_place[0] += self.base.place[0] + 1
                self.unit_list[len(self.unit_list) - 1].unit_place[1] = self.base.place[1]
                self.unit_button(self.unit_list[len(self.unit_list) - 1].unit_place[0],
                                 self.unit_list[len(self.unit_list) - 1].unit_place[1],
                                 cell_size, self.name)

    def push_highlighted_cell(self):
        pass

    def highlighted_cell(self, x, y, cell_size, nickname):
        self.unit_list[len(self.unit_list) - 1]. \
            highlighted_cell = UI.HighlightedCellButton(10 + x * cell_size - cell_size // 2,
                                        100 + y * cell_size - cell_size // 2,
                                        self.push_highlighted_cell,
                                        self.unit_list[len(self.unit_list) - 1].type,
                                        nickname)

    def push_unit_button(self, x, y, cell_size, nickname):
        self.highlighted_cells_list = []
        self.highlighted_cell(x + 1, y, cell_size, nickname)

    def count_units(self, text):
        print('{} have {} units'.format(text, self.units.amount))

    def info_about_units(self, text):
        s = 'Information about \nunits of player {}:\n'.format(self.name)
        s += 'Fraction: {}\n'.format(text)
        for i in self.unit_list:
            s += 'Unit: {}, damage: {}, hp: {}, placed on: {}\n'.format(i.type, i.damage, i.hp, i.unit_place)
        s += 'Base is placed on: {}\n'.format(self.base.place)
        s += '{} have {} units'.format(text, self.units.amount)
        return s


class CriminalFraction(Fraction):
    def __init__(self):
        super().__init__()
        self.name_units.append(Bariga)
        self.name_units.append(Bydlan)
        self.name_units.append(Offnik)
        self.name_units.append(Zek)

    def info_about_units(self):
        return super().info_about_units("Criminals")

    def count_units(self):
        super().count_units("Criminals")


class Bydlan(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Bydlan'


class Bariga(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 3
        self.type = 'Bariga'


class Offnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 5
        self.type = 'Offnik'


class Zek(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 7
        self.type = 'Zek'


###############################################################NEXTFRACTION###############
class MajorsFraction(Fraction):
    def __init__(self):
        super().__init__()
        self.name_units.append(Podsosnik)
        self.name_units.append(Pokazushnik)
        self.name_units.append(Major)
        self.name_units.append(MainMajor)

    def count_units(self):
        super().count_units('Majors')

    def info_about_units(self):
        return super().info_about_units("Majors")


class Podsosnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.hp = 2
        self.type = 'Podsosnik'


class Pokazushnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Pokazushnik'


class Major(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 4
        self.type = 'Major'


class MainMajor(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 6
        self.type = 'MainMajor'


###############################################################NEXTFRACTION###############
class PartyFraction(Fraction):
    def __init__(self):
        super().__init__()
        self.name_units.append(Fan)
        self.name_units.append(Modnik)
        self.name_units.append(Strelocnik)
        self.name_units.append(Misha)

    def count_units(self):
        super().count_units("Party")

    def info_about_units(self):
        return super().info_about_units("Party")


class Fan(Units):
    def __init__(self):
        super().__init__()
        self.damage = 3
        self.hp = 1
        self.type = 'Fan'


class Modnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Modnik'


class Strelocnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 4
        self.type = 'Strelocnik'


class Misha(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 9
        self.type = 'Misha'


###############################################################NEXTFRACTION###############
class BotansFraction(Fraction):
    def __init__(self):
        super().__init__()
        self.name_units.append(Dohodyaga)
        self.name_units.append(Otlychnik)
        self.name_units.append(Tupoydrug)
        self.name_units.append(Lubimchik)

    def count_units(self):
        super().count_units("Botans")

    def info_about_units(self):
        return super().info_about_units("Botans")


class Dohodyaga(Units):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.hp = 1
        self.type = 'Dohodyaga'


class Otlychnik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 2
        self.hp = 2
        self.type = 'Otlychnik'


class Tupoydrug(Units):
    def __init__(self):
        super().__init__()
        self.damage = 1
        self.hp = 12
        self.type = 'Tupoydrug'


class Lubimchik(Units):
    def __init__(self):
        super().__init__()
        self.damage = 4
        self.hp = 1
        self.type = 'Lubimchik'
