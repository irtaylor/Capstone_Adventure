#!/usr/bin/env python

import text_helpers
from cmd import Cmd
from rm_player import Player
from parser_grammar import *
from rm_item import Item



def convert_to_key(world_name):
    """
    Converts the given World name into the key that's used in the my_worlds dictionary
    :param world_name: The world name as a string
    :return: The world name as it appears as a key in the my_worlds dictionary
    """
    lower_case = world_name.lower()
    key = lower_case.replace(" ", "_")
    return key

# ################## This whole block to be deleted when Item subclasses are implemented #############
# This is just to keep the code functional while the Item subclasses are being implemented
# JSON support
import json
from pprint import pprint

OBJECTS_PATH = './data/items/'




class CommandParser(Cmd):

    def __init__(self, worlds_map):
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
        self.current_world = None
        self.current_room = None

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
        print "Press any ENTER to continue..."
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
        args = args.lower()
        # check if portal gun -- portal gun is special case item, so hard coding how it responds
        if args == 'portal gun':
            for world in self.player.worlds:
                print self.player.worlds[world].name
        # not portal gun to use item action text
        #else:
            # TODO: fix so that it retrieves item from dictionary, not instantiate item
            # Commenting out non portal gun items use()
            # self.item = Item(args)
            # print self.item.use()

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
        if convert_to_key(destination) in self.worlds.keys():
            return True, False, destination

        # Else, return (!is_valid, !is_room, None)
        else:
            return False, False, None

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
        print "You can go to the following rooms: "
        for room in self.current_world.rooms:
            print room
        self.list_room_items()

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

    # populate array of things in the current room
    # this is necesary now because the items and features are stored in two different locations and have different information available
    # formats strings to prepend article and determine plurality
    def get_room_elements(self, room_elements):   
        for element in self.current_room.get_items():
            fixed_string = format_string_plurality(self.get_item_name(element), None)
            room_elements.append(fixed_string)
        for feature in self.current_room.get_features():
            fixed_string = format_string_plurality(feature["key"], feature["description"])
            room_elements.append(fixed_string)
        return room_elements

    def get_item_description(self, item):
        try:
            self.my_items[item]["description"]
        except:
            with open(OBJECTS_PATH + item.lower() + '.json') as json_data:
                data = json.load(json_data)
            json_data.close()
            return data["description"]
        else:
            return self.my_items[item]["description"]
            
    def get_item_name(self, item):
        try:
            self.my_items[item]["name"]
        except:
            with open(OBJECTS_PATH + item.lower() + '.json') as json_data:
                data = json.load(json_data)
            json_data.close()
            return data["name"]
        else:
            return self.my_items[item]["name"]

    def build_sentence(self, elements):
        """
        Builds sentence to return to output to the user appending conjunctions, commas, and helping verbs as needed
        """
        sentence = "There"
        if (len(elements)) == 0:
                sentence+=" is nothing of note here."
        else:
            # print first element
            # determine appropriate verb
            if elements[0].startswith("some"):
                sentence += " are "
            else:
                sentence += " is "
            sentence+=elements[0]
            # for all but last element, print with comma
            for element in elements[1:-1]:
                sentence+=", "
                sentence+=element
            if len(elements) > 1:
                sentence+=" and "
                sentence+=elements[-1]
        print sentence + "."

    def list_room_items(self):
        """
        Collects elements (items and features) from room and their descriptions
        Formats the text sentence and outputs it to user
        """
        room_elements = []
        room_elements = self.get_room_elements(room_elements)
        self.build_sentence(room_elements)


    def do_go(self, args):
        """
        Updates the player's location to that given in the user's input, if valid.
        :param args: String argument given after the command "go"
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
                new_world = convert_to_key(stripped)
                self.player.set_current_world(self.worlds[new_world])

        # Otherwise, destination was invalid, scold Morty for being useless.
        else:
            print "What are you blathering about Morty? " \
                  "Are you sure that's even a real place? There's no %s around here!" % stripped

    def do_port(self, args):
        """
        Executes the body of do_go().
        """
        self.do_go(args)

    def do_get_current_world(self, args):
        """State the player's current world and room """
        print self.player.get_current_world()


    def do_get(self, args):
        #Utility verb, currently used to get current world
        """ State the player's current world and room """
        if (args == 'current world'):
            print self.player.get_current_world()

    def do_list(self, args):
        if (args == 'inventory'):
            """ List the player's inventory """
            print "Current Inventory:"
            for item in self.player.get_inventory():
                print "- %s" % self.get_item_name(item)

    #TODO: Can probably remove this; was a test verb, is no longer needed
    def do_list_inventory(self, args):
        """List the player's inventory """
        print "Current Inventory:"
        for item in self.player.get_inventory():
            print '- ' + item

    def do_inventory(self, args):
        """List the player's inventory"""
        """Required verb."""
        self.do_list("inventory")

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_shoot(self, args):
        """Shoots raygun."""
        """    With args: shoots target (maybe? unsure how combat system will work).  Might get rid of this action in favour for a general use item.
            Without args: Error text.
        """
        print "Not yet implemented."
        # Item class not implemented yet
        #item = Item('ray gun')
        #print item.use()
        
    def do_portal(self, args):
        """
        With args: Error text.
        Without args: Check portal gun for fuel and chips.
        """
        if len(args) == 0:
            print "Where are you going?"
        else:
            name = args
            print "Check portal gun for fuel and chips.\n" \
                  "Do we want it to check for chips or did we " \
                  "want to have it blow up instead?\n" % name

    def do_look(self, args):
        """
        With no args: Reprints the long form description of the room.
        With args: Prints description of a feature or object.
        Required verb.
        """
        if len(args) == 0:
            print self.current_room.get_entrance_long()
        # Required verb. Check args for 'at', if look at, validate the item is a valid item or object then print
        # the description of object or item
        else:
            # strip off preposition
            stripped_input = check_for_prepositions(args)
            # iterate through words in string
            # check if valid item in player inventory
            for word in stripped_input:
                if self.is_item_valid(word, self.player.get_inventory()) is True:
                    item = convert_to_key(stripped_input)
                    print self.get_item_description(item)
                    return

            # check if valid item in current room        
            for word in stripped_input:
                if self.is_item_valid(word, self.current_room.get_items()) is True:
                    item = convert_to_key(stripped_input)
                    print self.get_item_description(item)
                    return

            # check if valid feature
            room_features = self.current_room.get_features()
            for word in stripped_input:
                for feature in room_features:
                    if word in feature["key"]:
                        print feature["interactive_text"]
                        return

            # TODO: Add error text for when user enters item not existing in the current room

    def is_item_valid(self, questionable_item, list_of_items):
        """
        Checks list to determine if item user is manipulating is in the list.
        """
        questionable_item = convert_to_key(questionable_item)
        for items in list_of_items:
            if questionable_item in items:
                return True
        return False
            
            
    def do_take(self, args):
        """
        Required verb.
        Take object and put in player's inventory.
        With args: Validate item is takeable (item exists in item database).  Throw error text if it isn't.
        Without args: Error text.
        """
        if len(args) == 0:
             print "You can't take everything!\n"
        else:
            #validate item exists, is in current room, etc
            # if so, add to player inventory, remove item from room           
            if self.is_item_valid(args, self.current_room.get_items()) is True:
                item = convert_to_key(args)
                self.current_room.remove_item(item)
                self.player.add_to_inventory(item)
            else:
                print "item is false"

    def do_drop(self, args):
        """
        Required verb.
        Take object out of player's inventory and drop on ground.
        With args: Validate item is droppable (item exists in player inventory).  Throw error text if it isn't.
        Without args: Error text.
        """
        if len(args) == 0:
             print "You can't take everything!\n"
        else:
            #validate item exists, is in current room, etc
            # if so, add to player inventory, remove item from room
            print self.player.get_inventory()
            if self.is_item_valid(args, self.player.get_inventory()) is True:
                item = convert_to_key(args)
                self.current_room.add_item(item)
                self.player.remove_from_inventory(item)
            else:
                print "item is false"
                
    def do_savegame(self, args):
        """
        Required verb.
        Saves game to file.
        """
        if len(args) == 0:
            print "Saving game...\n"

    def do_loadgame(self, args):
        """
        Require verb.
        Load game.  Do we want to enable a parameter for the player to name the save file?
        """
        if len(args) == 0:
            print "Loading file, if file doesn't exist, throw error text.\n"

    def default(self, args):
    # TODO: Check out aliasing http://stackoverflow.com/questions/12911327/aliases-for-commands-with-python-cmd-module
        print "Not a recognized command"

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit
