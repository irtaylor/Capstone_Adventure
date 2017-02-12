"""
Kyle Bergman
cs419
Rick and Morty Adventure Game: Keep Summer Safe
Benjamin Brewster
"""

from rm_item import Item


class Player(object):

    def __init__(self):
        """
        Initializes the player with an empty inventory.
        """
        self.inventory = {}
        self.current_world = None
        self.current_room = None

    def add_to_inventory(self, item):
        """
        Adds the given Item object to the player's inventory.
        :param item: The Item object to be added to the inventory.
        """
        self.inventory[item] = item

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

    def attack(self):
        """
        Attack in battle.
        :return: an integer representing the strength of the attack.
        """
        pass

    def ask_morty(self):
        """
        Ask Morty for help even though he will probably say something useless.
        :return: a string representing Morty's comments.
        """
        pass
