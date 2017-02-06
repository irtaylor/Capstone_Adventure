#!/usr/bin/env python

from cmd import Cmd

import sys
import re
from rm_player import Player
from rm_item import Item
from rm_world import World
from rm_room import Room

PREPOSITIONS = { 'to' }
CONJUNCTIONS = { 'and' }


def spaceToUnderscore(mystring):
    return mystring.replace(" ", "_")
    
def underscoreToSpace(mystring):
    return mystring.replace("_", " ")
    
def prepCheck(mystring):
    if mystring.split()[0] in PREPOSITIONS:
            mystring = mystring.split(' ')[1:]
            mystring = " ".join(mystring)
    return mystring

class CommandParser(Cmd):
    prompt = '>> '
    player = Player()

    #args = args.lower()
      
    def do_use(self, args):
        """ Calls corresponding use command for the item in question """
        args = args.lower()
        #check if portal gun -- portal gun is special case item, so hard coding how it responds
        if (args == 'portal gun'):
            for world in self.player.worlds:
                print self.player.worlds[world].name
        #not portal gun to use item action text
        else:
            self.item = Item(args)
            print self.item.use()
    
    def do_get_current_world(self, args):
        """ State the player's current world and room """
        print self.player.get_current_world()
    
    def do_get(self, args):
        """ State the player's current world and room """
        if (args == 'current world'):
            print self.player.get_current_world()

    def do_list(self, args):
        if (args == 'inventory'):
            """ List the player's inventory """
            print "Current Inventory:"
            for item in self.player.get_inventory():
                print '- ' + item

    def do_go(self, args):
        #split off preposition if there is one
        args = prepCheck(args)
        args = spaceToUnderscore(args).lower()
        self.player.set_current_world(self.player.worlds[args])
        self.item = Item('portal gun')
        print self.item.use()

    def do_port(self, args):
        self.do_go(args)
        
    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_shoot(self, args):
        """Shoots raygun.
            With args: shoots target (maybe? unsure how combat system will work).  Might get rid of this action in favour for a general use item.
            Without args: Error text."""
        item = Item('ray gun')
        print item.use()

    def do_look(self, args):
        """Required verb.
        With no args: Reprints the long form description of the room.
        With args: look at a feature or object."""
        if len(args) == 0:
            sys.stdout.write(self.data["longform"] + '\n')
        else:
            '''Required verb. Check args for 'at', if look at, validate the item is a valid item or object then print the description of object or item'''
            '''Need to implement for loop for cycling through lists of objects,'''
            sys.stdout.write('Looks like there is a %s lying around.\n' % self.data["objects"][0])

    def do_take(self, args):
        """Required verb.
        Take object and put in player's inventory.
        With args: Validate item is takeable (item exists in item database).  Throw error text if it isn't.
        Without args: Error text."""
        if len(args) == 0:
             print "You can't take everything!\n"
        else:
            name = args

    def do_savegame(self, args):
        """Required verb.
        Saves game to file."""
        if len(args) == 0:
            print "Saving game...\n"

    def do_loadgame(self, args):
        """Require verb.
        Load game.  Do we want to enable a parameter for the player to name the save file?"""
        if len(args) == 0:
            print "Loading file, if file doesn't exist, throw error text.\n"
    
    def default(self, args):
        print "Not a recognized command"

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit
