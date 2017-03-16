#!/usr/bin/env python

import text_helpers
import gameover
from cmd import Cmd
from parser_grammar import *
from rm_save import *
from rm_load import *

SAVE_FILE_DIRECTORY_PATH = "data/savegame"


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
                        'examine' : 'look',
                        'grab' : 'take',
                        'pick' : 'take',
                        'port' : 'go',
                        'portal' : 'go',
                        'leave' : 'drop' ,
                        'fix' : 'recharge',
                        'squanch' : 'use',
                        'exit' : 'quit'}

    def default(self, line):
        line = check_for_prepositions(line)
        cmd, cmd_arg = line.split()[0], " ".join(line.split()[1:])
        key = text_helpers.convert_to_key(cmd_arg)
        # check if the command is a known alias
        if cmd in self.aliases:
            getattr(self, ('do_' + self.aliases[cmd]))(cmd_arg)
            return

        # check if the command can apply to a room feature
        for feature in self.player.current_room.features:
            if cmd_arg == feature["key"] or convert_to_key(cmd_arg) == feature["key"]:
                # found feature in room, check for the correct action
                for action in feature["actions"]:
                    if cmd in action:
                        print action[cmd]
                        return

        # check if the command applies to an item
        if key in self.player.inventory:
            if key in self.items.keys():
                self.items[key].use(self.current_world, self.current_room)
                return

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
        ending = gameover.check_for_ending(self)
        if ending:
            text_helpers.get_ending(ending)
            print "Press ENTER to continue..."
            self.stdin.readline()
            stop = True
            return stop

        self.sync_location()

    def do_use(self, args):
        """ Calls corresponding use command for the item in question """
        stripped = check_for_prepositions(args)
        key = text_helpers.convert_to_key(stripped)
        if key == 'portal_gun' or key == 'processor' or key == 'processors':
            print 'It\'s a Big Multiverse, Morty. But without more processors, we can only go here:'
            for world in self.player.unlocked_worlds:
                print self.worlds[world].name
        elif key not in self.player.inventory:
            print "You know, Morty, it might be useful to use that if we actually had it. But alas, we do not. " \
                  "So next time how about you suggest something useful."
        elif key in self.items.keys():
            self.items[key].use(self.current_world, self.current_room)
            if self.items[key].num_uses == 0 and self.items[key].is_rechargeable is False:
                self.player.remove_from_inventory(key)

    def is_valid_destination(self, destination):
        """
        Determines whether the given destination is a valid one given where the player currently is.
        :param destination: String name of the destination. This will be either a World dictionary key or Room name.
        :return: A Tuple of length 3 (is_valid_destination, is_room, associated key string)
        """
        # If the given destination is a room in our current world, return (is_valid, is_room, key)
        for key in self.current_world.rooms.keys():
            room_name = self.current_world.rooms[key].name
            if room_name.lower() == destination.lower():
                return True, True, key

        # If the destination is a key in our worlds map, return (is_valid, !is_room, key)
        if text_helpers.convert_to_key(destination) in self.player.unlocked_worlds:
            return True, False, destination
        # Else, return (!is_valid, !is_room, None)
        else:
            return False, False, None

    def print_rooms_list(self):
        """
        Print rooms that the player can navigate to in the current world
        """
        if len(self.current_world.rooms) > 1:
            print "You can go to the following rooms from here: "
            for key in self.current_world.rooms.keys():
                room = self.current_world.rooms[key]
                if room.name != self.current_room.name:
                    print room.name
            print

    def change_world(self):
        """
        Updates the user to their newest location and prints out descriptions, features, items, etc.
        """
        # print exit text from current room
        if self.current_room is not None:
            self.current_room.print_exit_description()
            # changing world, so must have used portal gun successfully, print portal gun message
            print self.items["portal_gun"].success_message

        # Update engine's current world to that of the player
        self.current_world = self.player.current_world

        # Get the starting room for the new world
        key = text_helpers.convert_to_key(self.current_world.name)
        start_name = convert_to_key(self.worlds[key].starting_room)
        start_room = self.worlds[key].rooms[start_name]

        # Update current room of both engine and player to world's starting room
        self.player.current_room = start_room
        self.current_room = start_room

        self.player.current_world.print_description()
        self.player.current_room.print_description()
        self.list_room_items()
        self.print_rooms_list()

    def change_room(self):
        """
        Updates the user to their newest room location and prints out relevant data/descriptions.
        """
        # print exit text from current room
        if self.current_room is not None:
            self.current_room.print_exit_description()

        # Update engine's current room to that of the player.
        self.current_room = self.player.current_room

        # Write out descriptions to player
        self.player.current_room.print_description()
        self.list_room_items()
        self.print_rooms_list()

    def do_recharge(self, key):
        """
        Recharges item using a battery.
        """
        key = text_helpers.convert_to_key(key)
        # check if item is in inventory
        if key not in self.player.inventory:
            print "What the hell are you talking about, Morty?  We don't have that."
        # check if item can be recharged
        elif self.items[key].is_rechargeable is False:
            print "Great, Morty, we'll just... just do... what?  We can't *urp* recharge that."
        # check if have battery in inventory
        elif self.is_item_valid("multiverse_battery", self.player.inventory) is False:
            print "Morty, we need a-a-a power source. " \
                  "You can't just go around saying random stuff and hoping it'll do something."
        # success, charge the item, remove the battery
        else:
            print self.items["multiverse_battery"].get_usable_description() + "%s." % self.items[key].get_name()
            self.items[key].num_uses += 5
            self.player.remove_from_inventory("multiverse_battery")

    def get_room_elements(self, room_elements):
        """
        populate array of things in the current room
        formats strings to prepend article and determine plurality
        """
        for element in self.current_room.get_items():
            fixed_string = format_string_plurality(self.items[element].get_name(), None)
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
        print

    def check_portal_gun_charge(self):
        """
        Verify portal gun is in player inventory and that it has sufficient charge to travel.
        """
        if self.items["portal_gun"].num_uses > 0:
                return True
        else:
            return False

    def do_go(self, args):
        """
        Usage: go [to planet|roomName]

        Let's get a move on, Morty! Summer most likely doesn't have much time left.
        """
        # split off preposition if there is one
        stripped = check_for_prepositions(args)

        if len(stripped) > 0:
            # Determine if the user's desired location is valid
            is_valid, is_room, destination = self.is_valid_destination(stripped)

            # If valid, change player's location to correct destination
            if is_valid is True:
                if is_room is True:
                    self.player.current_room = self.current_world.rooms[destination]

                else:
                    # check portal gun is in inventory and has sufficent charge
                    if "portal_gun" not in self.player.inventory:
                        print "W-w-we left the portal gun behind, Mo*URPPP*rty. It seemed like a stupid idea at the time, and now it seems even stupider."
                    elif self.check_portal_gun_charge() is True:
                        new_world = text_helpers.convert_to_key(stripped)
                        self.player.set_current_world(self.worlds[new_world])
                        self.items["portal_gun"].num_uses -= 1
                        if self.items["portal_gun"].num_uses <= 2:
                            print "Woah, be careful. Portal gun's a little low on charge, and I do NOT want to get stranded with you!"
                    # gun is out of juice, return error text
                    else:
                        print self.items["portal_gun"].get_cannot_use_description()

            # Otherwise, destination was invalid, scold Morty for being useless.
            else:
                print "What are you blathering about Morty? " \
                      "Are you sure that's even a real place? There's no %s around here!" % stripped
        else:
            print "Yes, but where Morty? You can't just say vague commands and expect me to know what you mean."

    def help_recharge(self):
        """
        Provides the user with witty, yet practical advice for recharging an item.
        """
        print '\nUsage: recharge [item]\n'
        print 'Uses batteries to power my engine and charge my phone and stuff.'

    def help_go(self):
        """
        Provides the user with witty, yet practical advice for going to another place.
        """
        print '\nUsage: go [to planet|roomName]\n'
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
            for item in self.player.inventory:
                if item == 'portal_gun':
                    print "- Portal Gun: Battery Level %d" % self.items[item].num_uses
                else:
                    print "- %s" % self.items[item].get_name()

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
            name = 'Morty'
        else:
            name = args
        print "Hello, %s. Sometimes it gets lonely traveling the Multiverse..." % name

    def help_hello(self):
        """
        Provides the user with witty, yet practical advice for saying hello.
        """
        print '\nUsage: hello [name]\n'
        print 'Morty sometimes I underestimate how socially inept you are. ' \
              'Do I really need to tell you how to say hello?'

    def do_look(self, args):
        """
        Prints a description of the item, feature, or room the player designates.
        """
        # strip off preposition
        stripped_input = check_for_prepositions(args)

        if len(stripped_input) == 0:
            print "Planet: " + self.current_world.name
            print "You are in the " + self.current_room.name + "."
            print
            print self.current_room.get_entrance_long()
            self.print_rooms_list()
            self.list_room_items()

        else:
            # iterate through words in string

            # check if valid item in player inventory
            if self.is_item_valid(stripped_input, self.player.inventory) is True:
                item = text_helpers.convert_to_key(stripped_input)
                print self.get_item_description(item)
                return

            # check if valid item in current room
            if self.is_item_valid(stripped_input, self.current_room.get_items()) is True:
                item = text_helpers.convert_to_key(stripped_input)
                print self.get_item_description(item)
                return

            # check if valid feature
            room_features = self.current_room.get_features()
            for word in stripped_input.split():
                for feature in room_features:
                    if word == feature["key"]:
                        print feature["interactive_text"]
                        print ("Hmmm, I wonder what we can do to a " + word + "?")   # give the user a list of actions they can take on a feature.
                        for action in feature["actions"]:
                            print "-", str(action.keys())[3:-2]
                        return

            # check if the feature key is two words (like tiny_rick)
            stripped_input = check_for_prepositions(args)
            stripped_input = convert_to_key(stripped_input)
            for feature in room_features:
                    if stripped_input == feature["key"]:
                        print feature["interactive_text"]
                        return

            print "What... what should I look at? Be specific, Morty."

    def is_item_valid(self, questionable_item, list_of_items):
        """
        Checks list to determine if item user is manipulating is in the list.
        """
        questionable_item = text_helpers.convert_to_key(questionable_item)
        for item in list_of_items:
            if questionable_item == item:
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
            # validate item exists, is in current room, etc
            # if so, add to player inventory, remove item from room
            if self.is_item_valid(args, self.current_room.get_items()) is True:
                item = text_helpers.convert_to_key(args)
                self.current_room.remove_item(item)

                if item == 'processor':
                    print "Added Processor to inventory."
                    self.add_processor_to_portal_gun()

                else:
                    self.player.add_to_inventory(item)
                    print "Added %s to inventory." % self.items[item].get_name()
            else:
                print "Don't be an idiot, we don't need that."

    def add_processor_to_portal_gun(self):
        """
        Adds processor to portal gun and unlocks new worlds, if eligible.
        """
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
            # validate item exists, is in current room, etc
            # if so, add to player inventory, remove item from room
            if text_helpers.convert_to_key(args) == "processor" or text_helpers.convert_to_key(args) == "processors":
                print "We can't drop Processors, Morty. They're fused into the Portal Gun. We can drop the Portal Gun, but... that's really stupid."
            elif self.is_item_valid(args, self.player.inventory) is True:
                item = text_helpers.convert_to_key(args)
                self.current_room.add_item(item)
                self.player.remove_from_inventory(item)
                print "Uh, I guess we can leave the  %s here. No idea why you'd want to do that though. Seems like we should be grabbing everything we *urp* can." % self.items[item].get_name()
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
            file_name = raw_input("Please enter a file name...")
        else:
            file_name = args

        savegame(file_name, self.worlds, self.items, self.player)

    def help_savegame(self):
        """
        Provides the user with witty, yet practical advice for how to save the current state of the game.
        """
        print '\nUsage: savegame\n'
        print 'Preserves the state of our universe into something I can carry in a flashdrive, Morty. ' \
              'I\'d explain more but I got shit to do.'


    def do_loadgame(self, args):
        """
        Loads a user's game file into the game engine and resumes the game.
        """

        if len(args) == 0:
            file_name = raw_input("Please enter a file name to load...")
        else:
            file_name = args

        path = SAVE_FILE_DIRECTORY_PATH + "/" + file_name
        if os.path.isdir(path):

            response = raw_input("Are you sure you want to abandon the current game and load this game? Say yes "
                                 "to confirm and anything else to abandon action.")

            if response.lower() == "yes":
                loadgame(path, self)
                self.do_look("")
        else:
            print "A save file under that name does not exist. Here are the current save files:"
            list = get_save_files()
            for save_file in list:
                if save_file != ".DS_Store":
                    print save_file

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
