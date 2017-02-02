"""
Kyle Bergman
cs419
Rick and Morty Adventure Game: Keep Summer Safe
Benjamin Brewster
"""


class Character(object):

    def __init__(self, name, attack_pwr, bribe_threshold):
        """
        Initializes the Character object.

        :param name: Name of the character
        :param attack_pwr: Attack Power of the character, should it be battled.
        :param bribe_threshold: How much money it takes to bribe this character
        """
        self.name = name
        self.attack_pwr = attack_pwr
        self.bribe_threshold = bribe_threshold
        self.description = ""
        pass

    def attack(self):
        """
        Attacks the player with a random strength between 0 and its attack power.

        :return: An integer representing its attack strength.
        """
        pass

    def get_description(self):
        """
        Describes the character to the player.

        :return: A string with the description.
        """
        pass

    def react_to_bribe(self, attempted_bribe):
        """
        Given the attempted bribe, the character will react.
        :param attempted_bribe: The amount of money the player is using in their bribe.
        """
        pass

    def negative_bribe_reaction(self):
        """
        Reacts poorly to the bribe. This can be in the form of attack or general standoffishness.
        """
        pass

    def positive_bribe_reaction(self):
        """
        React moderately well to the bribe. This could be in the form of an item, processor chip,
        or advice.
        :return: Results may vary by character
        """
        pass
