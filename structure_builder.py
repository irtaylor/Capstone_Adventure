#!/usr/bin/env python

import json
import os
from rm_room import Room
from rm_world import World

WORLDS_DIRECTORY_PATH = "data/worlds/"


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
            if len(current_room.features) > 0:
                if current_room.features[0] is not None and type(current_room.features[0]) is dict:
                    # TODO: HEY LOOK HERE
                    print current_room.features[0]["key"]
            if current_room.items is not None:
                print current_room.items
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
        # TODO: Remove this check because all rooms should have an items array, even if empty
        if data.get("items") is not None:
            new_room.items = data["items"][:]
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
        new_world.connections = data["connections"][:]
        return new_world
