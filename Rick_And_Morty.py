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

demo_room_path = './data/rooms/earth/living_room.json'
WORLDS_FILE_PATH = "data/worlds/"
ROOMS_FILE_PATH = "data/rooms/"
prompt_enter = "Press ENTER to continue..."
MY_WORLDS = {}


def construct_worlds():
    global MY_WORLDS
    world_files = os.listdir(WORLDS_FILE_PATH)
    for world in world_files:
        str_key = world[:-5]
        world_obj = build_world(WORLDS_FILE_PATH + world)
        MY_WORLDS[str_key] = world_obj
    room_files = os.listdir(ROOMS_FILE_PATH)
    for world in room_files:
        if world in MY_WORLDS:
            corresponding_world = MY_WORLDS[world]
            areas = os.listdir(ROOMS_FILE_PATH + world)
            for area in areas:
                if area[-5:] == ".json":
                    path = ROOMS_FILE_PATH + world + "/" + area
                    new_area = build_room(path)
                    corresponding_world.rooms.append(new_area)


def print_worlds():
    global MY_WORLDS
    for world in MY_WORLDS:
        planet = MY_WORLDS[world]
        print planet.name
        print planet.description
        for room in planet.rooms:
            print room.name
            print room.long_description
        print "\n"


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

        demo_room = build_room(demo_room_path)
        sys.stdout.write(demo_room.name + '\n')
        sys.stdout.write(demo_room.get_entrance_long() + '\n')

        helloparser.cmdloop()

    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    #construct_worlds()
    #print_worlds()
    main()
