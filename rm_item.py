"""
Kyle Bergman
cs419
Rick and Morty Adventure Game: Keep Summer Safe
Benjamin Brewster
"""


class Item(object):

    def __init__(self):
        """
        Initializes the Item object
        :param num_uses: The number of times that this item may be used
        """
        # self.num_uses = num_uses
        self.name = ''

    def get_name(self):
        """
        :return: Returns the name of this Item.
        """
        return self.name

    def use(self, room, in_battle, health):
        """
        A player uses the item. Results may vary.

        :param room: The room the player is currently in.
        :param in_battle: Whether the player is trying to use this in battle.
        :param health: How much health the player has.
        :return: This may vary depending on the item.
        """
        pass

    def get_usable_description(self):
        """
        When this item is usable, the player will receive this message.
        :return: A string with the description.
        """
        pass

    def get_cannot_use_description(self):
        """
        When this item is not usable, the player will receive this message.
        :return: A string with the description.
        """
        pass
