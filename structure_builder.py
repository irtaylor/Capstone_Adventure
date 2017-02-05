"""
Kyle Bergman
cs419
Rick and Morty Adventure Game: Keep Summer Safe
Benjamin Brewster
"""
import json
from rm_room import Room
from rm_world import World


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
        # new_room.items = data["objects"][:]
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
        new_world.description = data["description"]
        new_world.connections = data["connections"][:]

        return new_world





