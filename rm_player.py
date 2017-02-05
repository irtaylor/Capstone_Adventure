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
        Initializes the player with an empty inventory, base attack power, and health.
        """
        self.inventory = {}
        self.current_world = None
        pass

    def add_to_inventory(self, item):
        self.inventory[item] = Item(item)

    def get_inventory(self):
        return self.inventory

    def get_current_world(self):
        return self.current_world.name

    def set_current_world(self, current_world):
        self.current_world = current_world


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
