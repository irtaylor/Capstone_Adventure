from cmd import Cmd
import sys
from rm_player import Player

roomdir = './formatted_data/rooms/'
worlddir = './formatted_data/worlds'

PREPOSITIONS = {'to'}
CONJUNCTIONS = {'and'}


def prepCheck(mystring):
    if mystring.split()[0] in PREPOSITIONS:
            mystring = mystring.split(' ')[1:]
            mystring = " ".join(mystring)
    return mystring


def convert_to_key(str):
    str = str.lower()
    str = str.replace(" ", "_")
    return str


class CommandParser(Cmd):

    def __init__(self, worlds_map):
        Cmd.__init__(self)
        self.prompt = '>> '
        self.player = Player()
        self.worlds = worlds_map
        self.current_world = None
        self.current_room = None

    def is_valid_destination(self, destination):
        for key in self.current_world.rooms.keys():
            if key.lower() == destination.lower():
                return True, True, key
        if convert_to_key(destination) in self.worlds.keys():
            return True, False, destination
        else:
            return False, False, None

    def change_world(self):
        # Update world of engine to that of the player
        self.current_world = self.player.current_world

        # Get the starting room for the new world
        key = convert_to_key(self.current_world.name)
        start_name = self.worlds[key].starting_room
        start_room = self.worlds[key].rooms[start_name]

        # Update current room of both engine and player to world's starting room
        self.player.current_room = start_room
        self.current_room = start_room

        # Write out descriptions to player
        # TODO: Add logic for if_visited to diff between long and short descriptions
        print self.player.current_world.description
        print self.player.current_room.get_entrance_long()
        for room in self.current_world.rooms:
            print room

    def change_room(self):
        # Update world of engine to that of the player
        self.current_room = self.player.current_room

        # Write out descriptions to player
        # TODO: Add logic for if_visited to diff between long and short descriptions
        print self.player.current_room.get_entrance_long()

    def preloop(self):
        if self.player.current_world.name != self.current_world:
            self.change_world()
        elif self.player.current_room != self.current_room:
            self.change_room()

    def postcmd(self, stop, line):
        if self.player.current_world != self.current_world:
            self.change_world()
        elif self.player.current_room != self.current_room:
            self.change_room()

    def do_go(self, args):
        # TODO: ADD VALIDATION LOGIC
        # TODO: ADD VALIDATION FOR TRAVELING TO SAME ROOM
        # split off preposition if there is one
        stripped = prepCheck(args)
        is_valid, is_room, destination = self.is_valid_destination(stripped)
        if is_valid is True:
            if is_room is True:
                self.player.current_room = self.current_world.rooms[destination]
            else:
                new_world = convert_to_key(stripped)
                self.player.set_current_world(self.worlds[new_world])
        else:
            print "What are you blathering about Morty? " \
                  "Are you sure that's even a real place? There's no %s around here!" % stripped

    def do_port(self, args):
        self.do_go(args)

    def do_use(self, args):
        """Calls corresponding use command for the item in question """

    def do_get_current_world(self, args):
        """State the player's current world and room """
        print self.player.get_current_world()

    def do_list_inventory(self, args):
        """List the player's inventory """
        print "Current Inventory:"
        for item in self.player.get_inventory():
            print '- ' + item

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_portal(self, args):
        """
        With args: Error text.
        Without args: Check portal gun for fuel and chips.
        """
        if len(args) == 0:
            print "Where are you going?"
        else:
            name = args
            print "Check portal gun for fuel and chips.\nDo we want it to check for chips or did we want to have it blow up instead?\n" % name

    def do_shoot(self, args):
        """
        Shoots raygun.
        With args: shoots target (maybe? unsure how combat system will work).  Might get rid of this action in favour for a general use item.
        Without args: Error text.
        """
        if len(args) == 0:
            print "Whoa, watch where you're pointing that thing!"
        else:
            name = args
            print "Shoot action goes here.\n"

    def do_look(self, args):
        """
        Required verb.
        With no args: Reprints the long form description of the room.
        With args: look at a feature or object.
        """
        if len(args) == 0:
            sys.stdout.write(self.current_room.get_entrance_long() + '\n')
        else:
            # Required verb. Check args for 'at', if look at, validate the item is a valid item or object then print
            # the description of object or item
            # Need to implement for loop for cycling through lists of objects
            sys.stdout.write('Looks like there is a %s lying around.\n' % str(self.current_room.get_items()))

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
            name = args

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

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit
