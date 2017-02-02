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
        pass

    def get_features(self):
        """
        Returns a list of the features in this Room.
        :return: A list of objects
        """
        pass

    def get_items(self):
        """
        Returns a list of items that are in this room, if any
        :return: A list of items in this room
        """
        pass

    def get_entrance_description(self):
        """
        When a player enters a room for the first time, they will receive this message.
        :return: A string with the long form description of this room.
        """
        pass

    def get_short_entrance_description(self):
        """
         When a player enters a room after the first time, they will receive this message.
        :return: A string with the short form description of this room.
        """
        pass

    def get_exit_description(self):
        """
        When a player exits a room for the first time, they will receive this message.
        :return: A string with the long form description of this room.
        """
        pass

    def get_short_exit_description(self):
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

    def get_adjacent_worlds(self):
        """
        Determine what worlds may be reached from this one.
        :return: A list of worlds that may be reached by the Portal Gun
        """
        pass

    def get_adjacent_rooms(self):
        """
        Determine where the Player may travel on this planet
        :return: A list of the rooms that a player may travel to.
        """
        pass



