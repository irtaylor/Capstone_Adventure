#!/usr/bin/env python

import curses

window = curses.initscr()
window.immedok(True)

try:
    window.border(0)

    (height, width) = window.getmaxyx()

    menuwin = curses.newwin(6, width - 12, height - 8, 5)
    menuwin.immedok(True)

    menuwin.box()
    #menuwin.addstr("Hello World of Curses!")

    window.getch()

except KeyboardInterrupt:
    pass
finally:
    curses.endwin()
