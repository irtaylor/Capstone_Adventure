#!/usr/bin/env python

class World(object):
    """
    A World in the Rick and Morty text adventure game is a container of different Room objects.
    """

    def __init__(self):
        """
        Initializes the Room.
        """
        self.name = ""
        self.key = ""
        self.rooms = {}
        self.starting_room = ""
        self.description = ""
        self.is_visited = False
        self.chips_needed = None

    def get_rooms(self):
        """
        Returns a list of the features in this Room.
        :return: A list of objects
        """
        return self.rooms

    def print_description(self):
        print "Planet: " + self.name
        if self.is_visited is False:
            print self.description
            self.set_is_visited(True)
        print

    def set_is_visited(self, is_visited):
        self.is_visited = is_visited

    def get_description(self):
        """
        :return: A string with the world's description.
        """
        return self.description
