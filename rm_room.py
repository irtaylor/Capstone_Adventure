"""
Kyle Bergman
cs419
Rick and Morty Adventure Game: Keep Summer Safe
Benjamin Brewster
"""


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
        self.features = []
        self.items = []
        self.long_description = ""
        self.short_description = ""
        self.is_visited = False
        self.features = {}
        # self.long_description_exit = ""
        # self.short_description_exit = ""
        # self.morty_hints = []
        # self.adjacent_rooms = []
        # self.adjacent_worlds = []

    def print_description(self):
        print self.name
        if self.is_visited is False:
            print self.long_description
            self.set_is_visited(True)
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
        :return: A string with the long form description of this room.
        """
        pass

    def get_exit_short(self):
        """
        When a player exits a room after the first time, they will receive this message.
        :return: A string with the short form description of this room.
        """
        pass

    def get_morty_hint(self):
        """
        When Rick requests advice from Morty, they will receive 1 of 3 random quotes from Morty
        with specific information about the room.
        :return: A string to be returned to the user.
        """
        pass

    def get_adjacent_rooms(self):
        """
        Determine where the Player may travel on this planet
        :return: A list of the rooms that a player may travel to.
        """
        pass
