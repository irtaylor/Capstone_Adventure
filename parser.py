from cmd import Cmd
import sys

roomdir = './formatted_data/rooms/'
worlddir = './formatted_data/worlds'

class MyPrompt(Cmd):

    prompt = '>> '
      
    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_port(self, args):
        """With args: Error text.
        Without args: Check portal gun for fuel and chips."""
        if len(args) == 0:
            print "Where are you going?"
        else:
            name = args
            print "Check portal gun for fuel and chips.\nDo we want it to check for chips or did we want to have it blow up instead?\n" % name
    
    def do_shoot(self, args):
        """Shoots raygun.
            With args: shoots target (maybe? unsure how combat system will work).  Might get rid of this action in favour for a general use item.
            Without args: Error text."""
        if len(args) == 0:
            print "Whoa, watch where you're pointing that thing!"
        else:
            name = args
            print "Shoot action goes here.\n"
    
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
           
    def do_help(self, args):
        """Required verb.
        Print available commands."""
        print "List of commands go here.\n"
    
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

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit
