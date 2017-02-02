"""
Kyle Bergman
cs419
Rick and Morty Adventure Game: Keep Summer Safe
Benjamin Brewster
"""


class Player(object):

    def __init__(self):
        """
        Initializes the player with an empty inventory, base attack power, and health.
        """
        self.inventory = []
        self.attack_pwr = 1
        self.health = 10
        pass

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
