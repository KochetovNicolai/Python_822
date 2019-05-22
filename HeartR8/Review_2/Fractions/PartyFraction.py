from Fractions.Units import Units
from UI.Buttons.Fraction import Fraction


class PartyFraction(Fraction):
    def __init__(self, field_size, width, height):
        super().__init__(field_size, width, height)
        self.name_units += [Fan, Modnik, Strelocnik, Misha]
        self.name_units_text += [Fan().type, Modnik().type, Strelocnik().type, Misha().type]
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

