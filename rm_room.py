#!/usr/bin/env python


class Room(object):
    """
    A Room in the Rick and Morty text adventure game is an area that exists in a World object.

    Rooms may have characters, features, items, and other secrets a player can find and
    interact with.
    """

    def __init__(self, name):
        """
        Initializes the Room.
        :param name: The name of the Room as a string
        """
        self.name = name
        self.key = ""
        self.features = []
        self.items = []
        self.hidden_items = []
        self.long_description = ""
        self.short_description = ""
        self.is_visited = False
        self.features = {}
        self.long_description_exit = ""
        self.short_description_exit = ""

    def print_description(self):
        print "You are in the " + self.name + "."
        if self.is_visited is False:
            print self.long_description
        else:
            print self.short_description

    def set_is_visited(self, is_visited):
        self.is_visited = is_visited

    def get_features(self):
        """
        Returns a list of the features in this Room.
        :return: A list of objects
        """
        return self.features

    def get_items(self):
        """
        Returns a list of items that are in this room, if any
        :return: A list of items in this room
        """
        return self.items

    def reveal_hidden_items(self):
        """
        Helper method used to transfer all items in the hidden array to that of the public, items array.
        """
        if len(self.hidden_items) > 0:
            while len(self.hidden_items) > 0:
                self.items.append(self.hidden_items.pop())
            return True
        return False
        
    def print_exit_description(self):
        """
        Prints exit description depending on if the room was previously visited or not
        """
        if self.is_visited is False:
            print self.get_exit_long()
        else:
            print self.get_exit_short()

    def get_entrance_long(self):
        """
        When a player enters a room for the first time, they will receive this message.
        :return: A string with the long form description of this room.
        """
        return self.long_description

    def get_entrance_short(self):
        """
         When a player enters a room after the first time, they will receive this message.
        :return: A string with the short form description of this room.
        """
        return self.short_description

    def get_exit_long(self):
        """
        When a player exits a room for the first time, they will receive this message.
        The is_visited flag is set when exiting the room the first time and the long message will no 
        longer be displayed upon subsequent visits.
        :return: A string with the long form description of this room.
        """
        self.set_is_visited(True)
        return self.long_description_exit

    def get_exit_short(self):
        """
        When a player exits a room after the first time, they will receive this message.
        :return: A string with the short form description of this room.
        """
        return self.short_description_exit

    def remove_item(self, item):
        """
        Removes item from room.
        """
        self.items.remove(item)

    def add_item(self, item):
        """
        Removes item from room.
        """
        self.items.append(item)
