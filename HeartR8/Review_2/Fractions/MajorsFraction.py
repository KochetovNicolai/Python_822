from Fractions.Units import Units
from UI.Buttons.Fraction import Fraction


class MajorsFraction(Fraction):
    def __init__(self, field_size, width, height):
        super().__init__(field_size, width, height)
        self.name_units += [Podsosnik, Pokazushnik, Major, MainMajor]
        self.name_units_text += [Podsosnik().type, Pokazushnik().type, Major().type, MainMajor().type]
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
