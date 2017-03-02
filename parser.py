#!/usr/bin/env python

import text_helpers
from cmd import Cmd
from rm_player import Player
from parser_grammar import *
from rm_item import Item


def convert_to_key(object_name):
    """
    Converts the given object name into the key that's used in their respective dictionary
    :param object_name: The object name as a string
    :return: The object name as it appears as a key in the dictionary
    """
    lower_case = object_name.lower()
    key = lower_case.replace(" ", "_")
    return key


class CommandParser(Cmd):

    def __init__(self, worlds_map, items_dictionary):
        """
        Initializes the Command Parser and field variables.
        :param worlds_map: Dictionary with name (string) --> World object pairings
        """
        # Call Base class's init function
        Cmd.__init__(self)

        # Initialize field variables
        self.prompt = '>> '
        self.player = Player()
        self.worlds = worlds_map
        self.items = items_dictionary
        self.current_world = None
        self.current_room = None
        self.aliases = { 'see' : 'look',
                        'grab' : 'take',
                        'pick' : 'take',
                        'port' : 'go',
                        'portal' : 'go'}

    def default(self, line):
        cmd, cmd_arg = line.split()[0], " ".join(line.split()[1:])
        if cmd in self.aliases:
            getattr(self, ('do_' + self.aliases[cmd]))(cmd_arg)
        else:
            print("This is tiring, Morty. Please, please just tell me something I understand.")


    def sync_location(self):
        """
        Synchronizes the player.current_world / room attribute with the world state
        """
        # If the player's current world doesn't match what's stored in the engine, update engine's world
        if self.player.current_world != self.current_world:
            self.change_world()

            # If the player's current room doesn't match what's stored in the engine, update engine's room
        elif self.player.current_room != self.current_room:
            self.change_room()

    def preloop(self):
        """
        Runs at the beginning of every game, initializes world with starting location.
        """
        text_helpers.get_intro()
        print "Press ENTER to continue..."
        self.stdin.readline()
        self.sync_location()

    def postcmd(self, stop, line):
        """
        Runs after each command. Updates engine's location if the user has changed locations.
        :param stop: EOF
        :param line: user input
        """
        self.sync_location()

    def do_use(self, args):
        """ Calls corresponding use command for the item in question """
        stripped = check_for_prepositions(args)
        key = convert_to_key(stripped)
        if key == 'portal_gun':
            print 'It\'s a Big Multiverse, Morty. But without more processors, we can only go here:'
            for world in self.player.unlocked_worlds:
                print self.player.worlds[world].name
        elif key not in self.player.inventory:
            print "You know, Morty, it might be useful to use that if we actually had it. But alas, we do not. " \
                  "So next time how about you suggest something useful."
        elif key in self.items.keys():
            self.items[key].use(self.current_world, self.current_room)

    def is_valid_destination(self, destination):
        """
        Determines whether the given destination is a valid one given where the player currently is.
        :param destination: String name of the destination. This will be either a World dictionary key or Room name.
        :return: A Tuple of length 3 (is_valid_destination, is_room, associated key string)
        """
        # If the given destination is a room in our current world, return (is_valid, is_room, key)
        for key in self.current_world.rooms.keys():
            if key.lower() == destination.lower():
                return True, True, key

        # If the destination is a key in our worlds map, return (is_valid, !is_room, key)
        if convert_to_key(destination) in self.player.unlocked_worlds:
            return True, False, destination
        # Else, return (!is_valid, !is_room, None)
        else:
            return False, False, None


    def print_rooms_list(self):
        """
        Print rooms that the player can navigate to in the current world
        """
        print "You can go to the following rooms: "
        for room in self.current_world.rooms:
            print room
        self.list_room_items()

    def change_world(self):
        """
        Updates the user to their newest location and prints out descriptions, features, items, etc.
        """
        # Update engine's current world to that of the player
        self.current_world = self.player.current_world

        # Get the starting room for the new world
        key = convert_to_key(self.current_world.name)
        start_name = self.worlds[key].starting_room
        start_room = self.worlds[key].rooms[start_name]

        # Update current room of both engine and player to world's starting room
        self.player.current_room = start_room
        self.current_room = start_room

        self.player.current_world.print_description()
        self.player.current_room.print_description()
        self.print_rooms_list()

    def change_room(self):
        """
        Updates the user to their newest room location and prints out relevant data/descriptions.
        """
        # Update engine's current room to that of the player.
        self.current_room = self.player.current_room

        # Write out descriptions to player
        # TODO: Add logic for if_visited to diff between long and short descriptions
        self.player.current_room.print_description()
        self.list_room_items()

    def get_room_elements(self, room_elements):
        """
        populate array of things in the current room
        formats strings to prepend article and determine plurality
        """
        for element in self.current_room.get_items():
            fixed_string = format_string_plurality(self.get_item_name(element), None)
            room_elements.append(fixed_string)
        for feature in self.current_room.get_features():
            fixed_string = format_string_plurality(feature["key"], feature["description"])
            room_elements.append(fixed_string)
        return room_elements

    def get_item_description(self, item):
        """
        Helper function.
        Collects item description from Item object or json file, whichever works.
        Can probably throw this away when Item subclasses are in.
        """
        try:
            self.items[item].description
        except:
            print "What? What are you saying?"
        else:
            return self.items[item].description

    def get_item_name(self, item):
        """
        Helper function.
        Collects item name from Item object or json file, whichever works.
        Can probably throw this away when Item subclasses are in.
        """
        try:
            self.items[item].name
        except:
            print "What? What are you saying?"
        else:
            return self.items[item].name

    def build_sentence(self, elements):
        """
        Builds sentence to output to the user appending conjunctions, commas, and helping verbs as needed
        """
        sentence = "There"
        if (len(elements)) == 0:
                sentence += " is nothing of note here."
        else:
            # print first element
            # determine appropriate verb
            if elements[0].startswith("some"):
                sentence += " are "
            else:
                sentence += " is "
            sentence += elements[0]
            # for all but last element, print with comma
            for element in elements[1:-1]:
                sentence += ", "
                sentence += element
            if len(elements) > 1:
                sentence += " and "
                sentence += elements[-1]
        print sentence + "."

    def list_room_items(self):
        """
        Collects elements (items and features) from room and their descriptions.
        Formats the text sentence and outputs it to user.
        """
        room_elements = []
        room_elements = self.get_room_elements(room_elements)
        self.build_sentence(room_elements)
        
    def do_testfunc(self,args):
        print self.items["portal_gun"].get_usable_description()
        
    def check_portal_gun(self):
        """
        Verify portal gun is in player inventory and that it has sufficient charge to travel.
        """
        if "portal_gun" in self.player.get_inventory():
            if self.items["portal_gun"].num_uses > 0:
                return True
        else:
            return False

    def do_go(self, args):
        """
        Usage: go [to planet|roomName]

        Let's get a move on, Morty! Summer most likely doesn't have much time left.
        """
        # TODO: ADD VALIDATION LOGIC
        # TODO: ADD VALIDATION FOR TRAVELING TO SAME ROOM
        # split off preposition if there is one
        stripped = check_for_prepositions(args)

        # Determine if the user's desired location is valid
        is_valid, is_room, destination = self.is_valid_destination(stripped)

        # If valid, change player's location to correct destination
        if is_valid is True:
            if is_room is True:
                self.player.current_room = self.current_world.rooms[destination]
            else:
                # check portal gun is in inventory and has sufficent charge
                if self.check_portal_gun() is True:
                    new_world = convert_to_key(stripped)
                    self.player.set_current_world(self.worlds[new_world])
                    self.items["portal_gun"].num_uses -= 1
                # gun is out of juice, return error text
                else:
                    print "No good, Morty, we're out of juice.  We need to find a power source to recharge the gun."

        # Otherwise, destination was invalid, scold Morty for being useless.
        else:
            print "What are you blathering about Morty? " \
                  "Are you sure that's even a real place? There's no %s around here!" % stripped

    def help_go(self):
        """
        Provides the user with witty, yet practical advice for going to another place.
        """
        print '\nUsage: go [to planet|roomName]\n'
        print 'Let\'s get a move on, Morty! Summer most likely doesn\'t have much time left.'

    def help_port(self):
        """
        Provides the user with witty, yet practical advice for porting to another place.
        """
        print '\nUsage: port [to planet|roomName]\n'
        print 'Let\'s get a move on, Morty! Summer most likely doesn\'t have much time left.'

    def help_use(self):
        """
        Provides the user with witty, yet practical advice for using an item.
        """
        print '\nUsage: use itemName\n'
        print 'Well Morty, if you have an item in your inventory, you can use it. ' \
              'Didn\'t think it was too complicated.'

    def do_get(self, args):
        """
        Helps the player determine where they are in the universe.
        """
        # TODO: strip arguments to include phrases like "get the current world", make more natural
        # TODO: add additional arguments for inventory?
        if args == 'current world':
            print self.player.get_current_world()

    def help_get(self):
        """
        Provides the user with witty, yet practical advice for seeing where they are.
        """
        print '\nUsage: get current world\n'
        print 'Uh, it seems in our scientific adventures, we lost track of which universe we are in. ' \
              'Use this command to pinpoint our location in the space time continuum.'

    def do_list(self, args):
        """
        A command for checking a player's inventory. The contents will be printed to the screen.
        """
        if args == 'inventory':
            print "Current Inventory:"
            for item in self.player.get_inventory():
                print "- %s" % self.get_item_name(item)

            print "- Processors: x%s" % self.player.num_chips

    def help_list(self):
        """
        Provides the user with witty, yet practical advice for checking their inventory.
        """
        print '\nUsage: list inventory\n'
        print 'WHAT\'S IN THE BOX, MORTY!? Just kidding, what have we gathered so far?'


    def do_inventory(self, args):
        """
        A command for checking a player's inventory. The contents will be printed to the screen.
        """
        self.do_list("inventory")

    def help_inventory(self):
        """
        Provides the user with witty, yet practical advice for checking their inventory.
        """
        print '\nUsage: inventory\n'
        print 'WHAT\'S IN THE BOX, MORTY!? Just kidding, what have we gathered so far?'

    def do_hello(self, args):
        """
        A simple echo function that says hello back to the user with an optional argument.
        """
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def help_hello(self):
        """
        Provides the user with witty, yet practical advice for saying hello.
        """
        print '\nUsage: hello [name]\n'
        print 'Morty sometimes I underestimate how socially inept you are. ' \
              'Do I really need to tell you how to say hello?'

    def help_portal(self):
        """
        Provides the user with witty, yet practical advice for porting to another place.
        """
        print '\nUsage: portal [to planetName]\n'
        print 'Feel the power, Morty. Feel the hyperbolic proton gravity thrusters charging this bad boy. ' \
              'Let\'s use the portal gun to find more of those chips!'

    def do_look(self, args):
        """
        Prints a description of the item, feature, or room the player designates.
        """
        # strip off preposition
        stripped_input = check_for_prepositions(args)

        if len(stripped_input) == 0:
            print self.current_room.get_entrance_long()
            self.print_rooms_list()

        else:
            # iterate through words in string

            # check if valid item in player inventory
            if self.is_item_valid(stripped_input, self.player.get_inventory()) is True:
                item = convert_to_key(stripped_input)
                print self.get_item_description(item)
                return

            # check if valid item in current room
            if self.is_item_valid(stripped_input, self.current_room.get_items()) is True:
                item = convert_to_key(stripped_input)
                print self.get_item_description(item)
                return

            # check if valid feature
            room_features = self.current_room.get_features()
            for word in stripped_input.split():
                for feature in room_features:
                    if word == feature["key"]:
                        print feature["interactive_text"]
                        return
            print "What... what should I look at? Be specific, Morty."

    def is_item_valid(self, questionable_item, list_of_items):
        """
        Checks list to determine if item user is manipulating is in the list.
        """
        questionable_item = convert_to_key(questionable_item)
        for items in list_of_items:
            if questionable_item in items:
                return True
        return False

    def help_look(self):
        """
        Provides the user with witty, yet practical advice for how to take items that exist in a room.
        """
        print '\nUsage: look [at feature|item]\n'
        print '*facepalm* Morty, se-s-seriously? You don\'t know how to look? You look at things.'

    def do_take(self, args):
        """
        Takes an item in a room and puts it in the player's inventory.
        """
        if len(args) == 0:
            print "What? What should I take, Morty? Give me something to work with."

        else:
            args = check_for_prepositions(args)
            #validate item exists, is in current room, etc
            # if so, add to player inventory, remove item from room
            if self.is_item_valid(args, self.current_room.get_items()) is True:
                item = convert_to_key(args)
                self.current_room.remove_item(item)

                if item == 'processor':
                    self.add_processor_to_portal_gun()

                else:
                    self.player.add_to_inventory(item)
                    print "Added %s to inventory." % self.get_item_name(item)
            else:
                print "Don't be an idiot, we don't need that."

    def add_processor_to_portal_gun(self):
        self.player.num_chips += 1
        for key in self.worlds.keys():
            current_world = self.worlds[key]
            if self.player.num_chips == current_world.chips_needed:
                self.player.unlocked_worlds.append(key)
                print "You've unlocked: %s" % current_world.name

    def do_drop(self, args):
        """
        Required verb.
        Take object out of player's inventory and drop on ground.
        With args: Validate item is droppable (item exists in player inventory).  Throw error text if it isn't.
        Without args: Error text.
        """
        args = check_for_prepositions(args)
        if len(args) == 0:
             print "What? What should I drop, Morty?"
        else:
            #validate item exists, is in current room, etc
            # if so, add to player inventory, remove item from room
            if self.is_item_valid(args, self.player.get_inventory()) is True:
                item = convert_to_key(args)
                self.current_room.add_item(item)
                self.player.remove_from_inventory(item)
                print "Dropped %s." % self.get_item_name(item)
            else:
                print "Can't drop that, Morty. No can do, nah-uh, no way!"

    def help_take(self):
        """
        Provides the user with witty, yet practical advice for how to take items that exist in a room.
        """
        print '\nUsage: take itemName\n'
        print 'A lot of my gadgets have been scattered around the universe, Morty. ' \
              'That\'s what happens when you do a lot of cool shit, instead of collecting stamps like Jerry.'

    def do_savegame(self, args):
        """
        Saves the game into a file that may be loaded later.
        """
        if len(args) == 0:
            print "Saving game...\n"

    def help_savegame(self):
        """
        Provides the user with witty, yet practical advice for how to save the current state of the game.
        """
        print '\nUsage: save\n'
        print 'Preserves the state of our universe into something I can carry in a flashdrive, Morty. ' \
              'I\'d explain more but I got shit to do.'

    def do_loadgame(self, args):
        """
        Loads a user's game file into the game engine and resumes the game.
        """
        if len(args) == 0:
            print "Loading file, if file doesn't exist, throw error text.\n"

    def help_loadgame(self):
        """
        Provides the user with witty, yet practical advice for how to load a game file.
        """
        print '\nUsage: load fileName\n'
        print 'We go back into that parallel universe we preserved. ' \
              'Hopefully in this one we can actually save Sarah, or whatever her name is.'

    def do_quit(self, args):
        """
        Usage: quit

        I always knew you were a quitter M-M-Morty. I bet you have some lame excuse like homework or something.
        """
        print "Quitting."
        raise SystemExit

    def help_quit(self):
        """
        Provides the user with witty, yet practical advice for how to use quit.
        """
        print '\nusage: quit\n'
        print 'I always knew you were a quitter M-M-Morty. I bet you have some lame excuse ' \
              'like homework or something.'
