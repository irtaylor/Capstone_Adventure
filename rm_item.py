#!/usr/bin/env python

# JSON support
import json
from pprint import pprint

from random import *

OBJECTS_PATH = './data/objects/'


class Item(object):

    def __init__(self, name):
        """
        Initializes the Item object
        :param num_uses: The number of times that this item may be used
        """
        # self.num_uses = num_uses
        self.name = name

    def get_name(self):
        """
        :return: Returns the name of this Item.
        """
        return self.name

    def use(self):
        """
        A player uses the item. Results may vary.

        :param room: The room the player is currently in.
        :param in_battle: Whether the player is trying to use this in battle.
        :param health: How much health the player has.
        :return: This may vary depending on the item.
        """
        seed()
        itemName = self.get_name().replace(" ", "_")
        with open(OBJECTS_PATH + itemName + '.json') as json_data:
            data = json.load(json_data)
        json_data.close()
        # need to add tag to item to determine if can fail, possibility to add a
        # different variable affecting difficulty to get a success
        if itemName != 'portal_gun':
            if randint(0,1) == 1:
                result = "success"
            else:
                result = "failure"
        else:
            result = "success"
        return data["actions"][result]

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
