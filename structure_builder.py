#!/usr/bin/env python

import json
import os
from rm_room import Room
from rm_world import World
from rm_item import Item

WORLDS_DIRECTORY_PATH = "data/worlds/"
ITEMS_DIRECTORY_PATH = "data/items"


def construct_worlds():
    """
    Populates World objects with JSON data from the "data/worlds" directory.

    :return: A dictionary with name(lower case, underscore-separated) --> world object pairs
    """
    # Dictionary to populate with key value pairs
    my_worlds = {}

    # List of directory names with our worlds
    world_directories = os.listdir(WORLDS_DIRECTORY_PATH)
    for directory in world_directories:
        if directory != ".DS_Store":
            # Key name for my_worlds
            str_key = directory

            # Create string representing the path to the world JSON file
            world_file_path = WORLDS_DIRECTORY_PATH + directory + '/' + directory + '.json'

            # Create world object and add to dictionary
            world_obj = build_world(world_file_path)
            my_worlds[str_key] = world_obj

            # Get names of all corresponding room JSON files
            room_directory = os.listdir(WORLDS_DIRECTORY_PATH + directory + '/rooms')

            # Create each Room object and append it to our list of rooms in the corresponding World object
            for room in room_directory:
                if room != ".DS_Store":
                    room_obj = build_room(WORLDS_DIRECTORY_PATH + directory + '/rooms/' + room)
                    world_obj.rooms[room_obj.name] = room_obj

    # Return our completed dictionary
    return my_worlds


def print_worlds(my_worlds):
    """
    Writes the contents of our my_worlds dictionary to standard out.

    :param my_worlds: Dictionary containing world name --> world obj pairs
    """
    for planet in my_worlds:

        # Get World object
        current_world = my_worlds[planet]

        # Print basic World info
        print current_world.name
        print current_world.description

        # Print basic room info
        room_keys = current_world.rooms.keys()
        for room in room_keys:
            current_room = current_world.rooms[room]
            print current_room.name
            print current_room.long_description
            """if len(current_room.features) > 0:
                if current_room.features[0] is not None and type(current_room.features[0]) is dict:
                    # TODO: HEY LOOK HERE
                    print current_room.features[0]["key"]"""
            print current_room.features
            print current_room.items
            """if current_room.items is not None:
                print current_room.items"""
        print "\n"


def build_room(file_path_str):
    """
    Loads a room's data from the given file, places it into a new Room object.

    :param file_path_str: path to the desired room file.
    :return: A new Room object with the content of the passed file
    """

    # Open the file if possible
    with open(file_path_str) as json_data:
        data = json.load(json_data)
        new_room = Room(data["name"])
        new_room.long_description = data["longform"]
        new_room.short_description = data["shortform"]
        new_room.features = data["features"][:]
        if data.get("items") is not None:
            new_room.items = data["items"][:]
        # TODO: REMOVE ONCE ALL ROOMS HAVE HIDDEN_ITEMS ARRAY, EVEN IF EMPTY
        if data.get("hidden_items") is not None:
            new_room.hidden_items = data["hidden_items"][:]
        if data.get("is_visited") is not None:
            new_room.hidden_items = data["is_visited"]
        return new_room


def build_world(file_path_str):
    """
    Loads a room's data from the given file, places it into a new Room object.

    :param file_path_str: path to the desired room file.
    :return: A new Room object with the content of the passed file
    """

    # Open the file if possible
    with open(file_path_str) as json_data:
        data = json.load(json_data)
        new_world = World()
        new_world.name = data["name"]
        new_world.starting_room = data["starting_room"]
        new_world.description = data["description"]
        new_world.chips_needed = data["chips_needed"]
        if data.get("key") is not None:
            new_world.key = data["key"]
        return new_world


def build_item(file_path_str):
    """
    Loads a item's data from the given file, places it into a new Item object.

    :param file_path_str: path to the desired item file.
    :return: A new Item object with the content of the passed file
    """

    # Open the file if possible
    with open(file_path_str) as json_data:
        data = json.load(json_data)
        new_item = Item()
        new_item.name = data["name"]
        new_item.description = data["description"]
        if data.get("actions") is not None:
            new_item.actions = data["actions"]
        if data.get("success_message") is not None:
            new_item.success_message = data["success_message"]
        if data.get("failure_messages") is not None:
            new_item.failure_messages = data["failure_messages"][:]
        if data.get("usable_world") is not None:
            new_item.usable_world = data["usable_world"]
        if data.get("usable_room") is not None:
            new_item.usable_room = data["usable_room"]
        if data.get("num_uses") is not None:
            new_item.num_uses = data["num_uses"]
        return new_item


def construct_items():
    """
    Populates Item objects with JSON data from the "data/items" directory.

    :return: A dictionary with name(lower case, underscore-separated) --> item object pairs
    """
    # Dictionary to populate with key value pairs
    my_items = {}

    # List of directory names with our items
    item_files = os.listdir(ITEMS_DIRECTORY_PATH)
    for item in item_files:
        if item != ".DS_Store":
            # Key name for my_worlds
            str_key = item[:-5]

            # Create string representing the path to the world JSON file
            item_file_path = ITEMS_DIRECTORY_PATH + '/' + item

            # Create the Item object given the file path
            item_obj = build_item(item_file_path)

            # Place the new item object into our dictionary
            my_items[str_key] = item_obj

    # Return our completed dictionary
    return my_items


def print_items(my_items):
    """
    Writes the contents of our my_items dictionary to standard out.

    :param my_items: Dictionary containing item name --> item obj pairs
    """
    for item in my_items:

        # Get World object
        current_item = my_items[item]

        # Print basic World info
        print current_item.name
        print current_item.description

        for action in current_item.actions:
            print action["name"]
            print action["success"]
            print action["failure"]
        print "\n"
