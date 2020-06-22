# See: https://docs.python.org/3.7/howto/curses.html

import curses

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

for y in range(0, 100):
    for x in range(0, 100):
        try:
            stdscr.addch(y, x, ord('.'))
        except curses.error:
            pass

stdscr.refresh()

x = y = 10

stdscr.addstr(x, y, "#", curses.color_pair(1))

while 1:
    c = stdscr.getch()

    if c == ord('q'):
        break

    stdscr.addstr(y, x, ".", curses.color_pair(1))

    if c == curses.KEY_RIGHT:
        x += 1
    elif c == curses.KEY_LEFT:
        x -= 1
    elif c == curses.KEY_UP:
        y -= 1
    elif c == curses.KEY_DOWN:
        y += 1

    stdscr.addstr(y, x, "#", curses.color_pair(1))

curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
