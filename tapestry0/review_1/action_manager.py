from actions import Fireball, Arrow, Pickaxe, Handaxe, HealingAura


def create_attack_action(action_name, origin, destination, damage=None, damage_factor=None):
    action = None
    if action_name == "fireball":
        action = Fireball(origin, destination)
    elif action_name == "arrow":
        action = Arrow(origin, destination)
    elif action_name == "pickaxe":
        action = Pickaxe(origin, destination)
    elif action_name == "handaxe":
        action = Handaxe(origin, destination)
    action.modifiers.set_damage(damage=damage, damage_factor=damage_factor)
    return action


def create_heal_action(action_name, recipient, heal=None, heal_factor=None):
    action = None
    if action_name == "healing aura":
        action = HealingAura(recipient)

    if action.modifiers.heal is None:
        action.modifiers.set_heal(heal=heal)
    if action.modifiers.heal_factor is None:
        action.modifiers.set_heal(heal_factor=heal_factor)
    return action


def kill_action(action):
    action.kill()
