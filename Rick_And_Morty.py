#!/usr/bin/env python
import sys
import os
from parser import *

import curses
from curses import wrapper
import textwrap

# JSON support
import json
from pprint import pprint

from structure_builder import *
from rm_player import Player



prompt_enter = "Press ENTER to continue..."
TEXT_PATH = "data/text/"

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


def get_text(file_name):
    file_path = TEXT_PATH + file_name
    with open(file_path, "r") as inFile:
        text = inFile.read().splitlines()
        for line in text:
            print line
        print

def get_intro():
    get_text("intro.txt")

def get_ending(ending_type):
    """
        Takes in the name of the desired ending (e.g. "plumbus" or "death"),
        and runs the corresponding ending.
    """
    ending_file_name = "ending_" + ending_type + ".txt"
    get_text(ending_file_name)


def main():
    my_worlds = construct_worlds()


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

        command_parser = CommandParser()
        command_parser.stdout = io
        command_parser.stdin = io

        #initializing player state
        command_parser.player.worlds = my_worlds
        command_parser.player.set_current_world(my_worlds["earth"])
        command_parser.player.add_to_inventory('Portal Gun')

        get_intro()
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
