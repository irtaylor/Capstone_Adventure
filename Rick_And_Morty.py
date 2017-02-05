#!/usr/bin/env python
import sys
import os
from parser import *

import curses
from curses import wrapper
import textwrap

# cmd.Cmd
from cmd import Cmd

# JSON support
import json
from pprint import pprint

from structure_builder import *


prompt_enter = "Press ENTER to continue..."


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
        temp = self.stdscr.getstr()
        if len(temp) == 0:
            temp = ' '
        return temp



def main():
    stdscr = curses.initscr()
    curses.cbreak()
    # curses.noecho()
    curses.echo()
    stdscr.keypad(1)
    stdscr.scrollok(True)
    stdscr.clear()
    stdscr.refresh()

    try:
        io = FakeStdIO(stdscr)
        sys.stdin = io
        sys.stdout = io

        helloparser = CommandParser()
        helloparser.stdout = io
        helloparser.stdin = io

        # game stuff goes here

        helloparser.cmdloop()

    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    construct_worlds()
    #print_worlds()
    main()
