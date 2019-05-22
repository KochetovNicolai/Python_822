from mapping import is_rocky, is_water
import config


class Modifiers:
    def __init__(self):
        self.exists = True
        self.damage = 0
        self.damage_factor = 1
        self.heal = 0
        self.heal_factor = 1

    def kill(self):
        self.exists = False

    def set_damage(self, *, damage=None, damage_factor=None):
        if damage is not None:
            self.damage = damage
        if damage_factor is not None:
            self.damage_factor = damage_factor

    def set_heal(self, *, heal=None, heal_factor=None):
        if heal is not None:
            self.heal = heal
        if heal_factor is not None:
            self.heal_factor = heal_factor

    def update(self):
        if self.exists:
            if self.damage * self.damage_factor < config.MODIFIERS_DAMAGE_LIMIT and \
                    self.heal * self.heal_factor < config.MODIFIERS_HEAL_LIMIT:
                self.kill()
            self.damage *= self.damage_factor
            self.heal *= self.heal_factor


class Action:
    def __init__(self):
        self.modifiers = Modifiers()
        self.physics = None

    def kill(self):
        self.modifiers.kill()

    def exists(self):
        return self.modifiers.exists

    def current_cell(self):
        return self.physics.current_cell()

    def update(self):
        self.modifiers.update()


class Bolt(Action):
    def __init__(self, creator, destination):
        super().__init__()
        self.creator = creator
        self.destination = destination

    def update(self):
        super().update()
        if is_rocky(self.current_cell()):  # no bolt penetrates mountains
            self.kill()


class Fireball(Bolt):
    def __init__(self, creator, destination):
        super().__init__(creator, destination)

    def update(self):
        super().update()
        if is_water(self.current_cell()):  # fireball is extinguished on water terrain
            self.kill()


class Arrow(Bolt):
    def __init__(self, creator, destination):
        super().__init__(creator, destination)


class Pickaxe(Bolt):
    def __init__(self, creator, destination):
        super().__init__(creator, destination)


class Handaxe(Bolt):
    def __init__(self, creator, destination):
        super().__init__(creator, destination)


class Aura(Action):
    def __init__(self, holder):
        super().__init__()
        self.holder = holder


class HealingAura(Aura):
    def __init__(self, recipient):
        super().__init__(recipient)
        self.modifiers.set_heal(heal=3, heal_factor=0.98)

    def update(self):
        if self.exists():
            self.holder.stats.hp += self.modifiers.heal
            super().update()
