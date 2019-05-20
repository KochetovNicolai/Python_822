from Fractions.Units import Units
from UI.Buttons.Fraction import Fraction


class CriminalFraction(Fraction):
    def __init__(self, field_size, width, height):
        super().__init__(field_size, width, height)
        self.name_units += [Bydlan, Bariga, Offnik, Zek]
        self.name_units_text += [Bydlan().type, Bariga().type, Offnik().type, Zek().type]
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
