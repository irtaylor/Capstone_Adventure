#!/usr/bin/env python
import random
from text_helpers import *

OBJECTS_PATH = './data/objects/'


class Item(object):

    def __init__(self):
        """
        Initializes the Item object
        """
        # self.num_uses = num_uses
        self.name = ""
        self.actions = []
        self.success_message = ""
        self.failure_messages = []
        self.usable_world = ""
        self.usable_room = ""
        self.num_uses = 0
        self.is_rechargeable = False

    def get_name(self):
        """
        :return: Returns the name of this Item.
        """
        return self.name

    def use(self, world, room):
        """
        A player uses the item. Results may vary.

        :param world: The world the player is exploring.
        :param room: The room the player is currently in.
        """
        if self.usable_world == convert_to_key(world.name) and self.usable_room == convert_to_key(room.name) \
                and self.num_uses > 0:

            if room.reveal_hidden_items() is True:
                print self.get_usable_description()
                self.num_uses -= 1
            else:
                print "Morty, we've already done that. We can't be wasting time!"
        else:
            print self.get_cannot_use_description()

    def get_usable_description(self):
        """
        When this item is usable, the player will receive this message.
        :return: A string with the description.
        """
        return self.success_message

    def get_cannot_use_description(self):
        """
        When this item is not usable, the player will receive this message.
        :return: A string with the description.
        """
        return random.choice(self.failure_messages)
