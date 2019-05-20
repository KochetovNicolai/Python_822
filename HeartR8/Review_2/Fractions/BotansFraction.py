from Fractions.Units import Units
from UI.Buttons.Fraction import Fraction


class BotansFraction(Fraction):
    def __init__(self, field_size, width, height):
        super().__init__(field_size, width, height)
        self.name_units += [Dohodyaga, Otlychnik, Tupoydrug, Lubimchik]
        self.name_units_text += [Dohodyaga().type, Otlychnik().type, Tupoydrug().type, Lubimchik().type]
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
