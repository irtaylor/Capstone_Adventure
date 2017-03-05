#!/usr/bin/env python


from rm_item import Item


class Player(object):

    def __init__(self):
        """
        Initializes the player with an empty inventory.
        """
        self.inventory = []
        self.current_world = None
        self.current_room = None
        self.unlocked_worlds = ["earth"]
        self.num_chips = 0

    def add_to_inventory(self, item):
        """
        Adds the given Item object to the player's inventory.
        :param item: The Item object to be added to the inventory.
        """
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        """
        Removes the given Item object from the player's inventory.
        :param item: The Item object to be removed from the inventory.
        """
        self.inventory.remove(item)

    def get_inventory(self):
        """
        :return: The dictionary representing item name --> Item object pairs
        """
        return self.inventory

    def get_current_world(self):
        """
        :return: Returns the name of the world that the player is on.
        """
        return self.current_world.name

    def set_current_world(self, current_world):
        """
        Updates location of the player.
        :param current_world: The World object the player is now exploring.
        """
        self.current_world = current_world

    def get_current_room(self):
        """
        :return: Returns the name of the room the player is in.
        """
        return self.current_room.name

    def set_current_room(self, current_room):
        """
        Updates location of the player.
        :param current_room: The Room object the player is now exploring.
        """
        self.current_room = current_room
