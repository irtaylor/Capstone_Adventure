"""
Kyle Bergman
cs419
Rick and Morty Adventure Game: Keep Summer Safe
Benjamin Brewster
"""
import json
import os
from rm_room import Room
from rm_world import World

WORLDS_DIRECTORY_PATH = "data/worlds/"


def construct_worlds():
    my_worlds = {}                                                                            # dictionary of all worlds
    world_directories = os.listdir(WORLDS_DIRECTORY_PATH)
    for directory in world_directories:
        str_key = directory                                                                     # remove .json from
        world_file_path = WORLDS_DIRECTORY_PATH + directory + '/' + directory + '.json'
        world_obj = build_world(world_file_path)
        my_worlds[str_key] = world_obj

        room_directory = os.listdir(WORLDS_DIRECTORY_PATH + directory + '/rooms')
        for room in room_directory:
            room_obj = build_room(WORLDS_DIRECTORY_PATH + directory + '/rooms/' + room)
            world_obj.rooms.append(room_obj)

    return my_worlds

def print_worlds(my_worlds):
    for world in my_worlds:
        planet = my_worlds[world]
        print planet.name
        print planet.description
        for room in planet.rooms:
            print room.name
            print room.long_description
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
