#!/usr/bin/env python

import sys
import os
from parser import *

import curses
from curses import wrapper
import textwrap

# JSON support - should be able to remove this
import json
from pprint import pprint

from structure_builder import *
from rm_player import Player

WORLDS_DIRECTORY_PATH = "data/worlds/"
ITEMS_DIRECTORY_PATH = "data/items"


class FakeStdIO(object):
    """
        A class to override write and readline methods for stdout and stdin respectively.
        This class utilizes a curses window to format text, wrapping it appropriately.

        This technique is demonstrated by AmstrongJ in his own text adventure game:
        Murder in the Park - A Robotic Mystery: https://github.com/ArmstrongJ/robotadventure
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def write(self, str):
        height,width = self.stdscr.getmaxyx()
        if len(str) >= width:
            for line in textwrap.wrap(str,width-2):
                self.stdscr.addstr(line)
                self.stdscr.addstr("\n")
        else:
            self.stdscr.addstr(str)
        self.stdscr.refresh()

    def readline(self):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.stdscr.attrset(curses.color_pair(1))
        temp = self.stdscr.getstr()
        if len(temp) == 0:
            temp = ' '
        self.stdscr.attrset(curses.color_pair(0))
        return temp


def main():
    my_worlds = construct_worlds(WORLDS_DIRECTORY_PATH)
    my_items = construct_items(ITEMS_DIRECTORY_PATH)
    # print_worlds(my_worlds)

    stdscr = curses.initscr()
    curses.start_color()
    curses.cbreak()
    # curses.noecho()
    curses.echo()
    stdscr.keypad(1)
    stdscr.scrollok(True)
    stdscr.clear()
    stdscr.refresh()

    io = FakeStdIO(stdscr)
    sys.stdin = io
    sys.stdout = io

    height, width = stdscr.getmaxyx()
    if (height < 24) or (width < 80):
        sys.stdout.write('Recommended minimum terminal size for this game is 80x24.\n')
        sys.stdout.write('Please resize your terminal and restart the game.\n')
        sys.stdout.write('Press ENTER to exit. Bye!\n')
        sys.stdin.readline()
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        sys.exit()


    try:
        command_parser = CommandParser(my_worlds, my_items)
        command_parser.stdout = io
        command_parser.stdin = io

        # initializing player state
        command_parser.player.worlds = my_worlds
        command_parser.player.set_current_world(my_worlds["earth"])
        command_parser.player.add_to_inventory('portal_gun')

        command_parser.cmdloop()

    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    main()
