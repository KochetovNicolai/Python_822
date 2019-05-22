from classes import Unit
from unit_physics import UnitPhysics
from actions import Bolt, Fireball, Handaxe, Arrow, Pickaxe, Aura, HealingAura
from action_physics import FireballPhysics, HandaxePhysics, ArrowPhysics, PickaxePhysics
from action_physics import HealingAuraPhysics


def physics_to_object(physics):
    return physics.get_object()


def object_to_physics(_object):
    return _object.physics


def attach_unit_physics(unit):
    if isinstance(unit, Unit):
        unit.physics = UnitPhysics(unit)


def update_unit_physics(unit):
    if isinstance(unit, Unit):
        unit.physics.update()


def kill_physics(_object):
    _object.physics.kill()


def attach_action_physics(action):
    if isinstance(action, Bolt):
        if isinstance(action, Fireball):
            action.physics = FireballPhysics(action, action.creator, action.destination)
        elif isinstance(action, Handaxe):
            action.physics = HandaxePhysics(action, action.creator, action.destination)
        elif isinstance(action, Arrow):
            action.physics = ArrowPhysics(action, action.creator, action.destination)
        elif isinstance(action, Pickaxe):
            action.physics = PickaxePhysics(action, action.creator, action.destination)
    elif isinstance(action, Aura):
        if isinstance(action, HealingAura):
            action.physics = HealingAuraPhysics(action)
    else:
        pass
