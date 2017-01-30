#!/usr/bin/env python

import sys

import curses
from curses import wrapper
import textwrap

# cmd.Cmd
from cmd import Cmd

# JSON support
import json
from pprint import pprint

demo_room_path = './data/demo.json'
prompt_enter = "Press ENTER to continue..."


class FakeStdIO(object):
    """
        A class to override write and readline methods for stdout and stdin respectively.
        This class utilizes a curses window to format text, wrapping it appropriately.
    """
    def __init__(self,stdscr):
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
        if len(temp)==0:
            temp = ' '
        return temp



class MyPrompt(Cmd):

    prompt = '>> '
    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit


def main():
    stdscr = curses.initscr()
    curses.cbreak()
    #curses.noecho()
    curses.echo()
    stdscr.keypad(1)
    stdscr.scrollok(True)
    stdscr.clear()
    stdscr.refresh()

    try:
        io = FakeStdIO(stdscr)
        sys.stdin = io
        sys.stdout = io

        helloparser = MyPrompt()
        helloparser.stdout = io
        helloparser.stdin = io

        # Print current room and prompt
        with open(demo_room_path) as json_data:
            data = json.load(json_data)
            #print(d)
            sys.stdout.write(data["name"] + '\n')
            sys.stdout.write(data["longform"] + '\n')

        helloparser.cmdloop()

    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

if __name__ == '__main__':
    main()
