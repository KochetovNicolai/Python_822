import classes, vars, functions



def screen_update(screen, items):
    screen.fill(vars.white)
    classes.oven.draw((200, 100))
    classes.farm.draw((200, 200))
    classes.factory.draw((200, 300))
    classes.extra_hand.draw((600, 100))
    classes.manipulator.draw((600, 200))
    classes.robot.draw((600, 300))
    functions.button_rectangle(screen, vars.fontObj1, 'Press Spacebar to make cookies.', vars.black, vars.white, (600, 400), 1)
    functions.button_rectangle(screen, vars.fontObj1, 'Press x10 to buy 10 items', vars.black, vars.white, (600, 430), 1)
    functions.button_rectangle(screen, vars.fontObj1, 'and Max to buy maximum amount of them.', vars.black, vars.white, (600, 460), 1)
    functions.button_rectangle(screen, vars.fontObj1, 'You have {} of cookies.'.format(round(vars.cookies, 2)), vars.black,
                               vars.white, (400, 10), 1)
    functions.button_rectangle(screen, vars.fontObj1, 'You gain {} of cookies per second'.format(round(
                             vars.cookies_income, 2)), vars.black, vars.white, (400, 40), 1)
    functions.button_rectangle(screen, vars.fontObj1, 'and {} of cookies per click.'.format(round(vars.cookies_per_click, 2)),
                               vars.black, vars.white, (400, 70), 1)
    functions.button_rectangle(screen, vars.fontObj1, 'You made {} clicks'.format(vars.clicks), vars.black, vars.white, (200, 550), 1)
    functions.button_rectangle(screen, vars.fontObj1, 'and cooked {} cookies.'.format(vars.all_cookies), vars.black,
                               vars.white, (200, 575), 1)
    functions.button_rectangle(screen, vars.fontObj2, 'Made by Sergey Dolgikh for his python project', vars.black,
                               vars.white, (600, 570), 1)
    functions.button_rectangle(screen, vars.fontObj2, 'Dolgoprudny, 2019', vars.black, vars.white, (600, 590), 1)

