import os
import json
from text_helpers import convert_to_key
from distutils.dir_util import copy_tree

SAVE_FILE_DIRECTORY_PATH = "data/savegame"
ITEMS_DIRECTORY_PATH = "data/items"
TEXT_DIRECTORY_PATH = "data/text"
WORLDS_DIRECTORY_PATH = "data/worlds"


def savegame(directory_name, worlds, items, player):
    """
    Saves the game as a new set of files in the "data/savegame" directory
    :param directory_name: Name of the new save file
    :param worlds: the dictionary of key-->world objects used in game
    :param items: the dictionary of key-->world objects used in game
    :param player: the player object showing the current state of the game
    """

    # Create directory for new save file
    path = SAVE_FILE_DIRECTORY_PATH + "/" + directory_name
    items_directory_path = path + "/items"
    if not os.path.exists(path):
        os.makedirs(path)

        # Create items directory and copy contents
        copy_directory(ITEMS_DIRECTORY_PATH, items_directory_path)

        # Create text directory and copy contents
        text_directory_path = path + "/text"
        copy_directory(TEXT_DIRECTORY_PATH, text_directory_path)

        # Create worlds directory and copy contents
        worlds_directory_path = path + "/worlds"
        copy_directory(WORLDS_DIRECTORY_PATH, worlds_directory_path)

    # Update contents of rooms
    for key in worlds.keys():
        world_obj = worlds[key]
        world_directory_path = path + "/worlds/" + key + "/rooms"
        update_room_files(world_obj, world_directory_path)

    # Update attributes of items
    update_item_files(items, items_directory_path)

    # Update player file
    create_player_file(player, path)


def create_player_file(player, path):
    """
    Creates a new json file with the attributes of the given player object.
    :param player: The object we want to convert to a json file
    :param path: Where we want to store the new player file
    """
    json_obj = dict()
    json_obj["current_world"] = convert_to_key(player.current_world.name)
    json_obj["current_room"] = convert_to_key(player.current_room.name)
    json_obj["inventory"] = player.inventory
    json_obj["num_chips"] = player.num_chips
    json_obj["unlocked_worlds"] = player.unlocked_worlds
    file_content = json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': '))

    with open(path + "/player.json", "w+") as json_data:
        json_data.write(file_content)


def update_room_files(world_obj, world_rooms_path):
    """
    Updates the room files for the given world with their current state as seen in game.
    :param world_obj: object holding the rooms
    :param world_rooms_path: the path to room files
    """
    file_list = [f for f in os.listdir(world_rooms_path) if f.endswith(".json")]

    # Clear previous room files
    for f in file_list:
        os.remove(world_rooms_path + "/" + f)

    # Create new room files
    for key in world_obj.rooms.keys():
        room = world_obj.rooms[key]
        create_room_file(room, world_rooms_path)


def create_room_file(room_obj, file_path):
    """
    Creates a new json file with the attributes of the given room object.
    :param room_obj: The object we want to convert to a json file
    :param file_path: Where we want to store the new room file
    """
    json_obj = dict()
    json_obj["name"] = room_obj.name
    json_obj["features"] = room_obj.features
    json_obj["items"] = room_obj.items
    json_obj["hidden_items"] = room_obj.hidden_items
    json_obj["longform"] = room_obj.long_description
    json_obj["shortform"] = room_obj.short_description
    json_obj["is_visited"] = room_obj.is_visited
    json_obj["long_description_exit"] = room_obj.long_description_exit
    json_obj["short_description_exit"] = room_obj.short_description_exit
    file_content = json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': '))

    file_name = convert_to_key(room_obj.name)
    with open(file_path + "/" + file_name + ".json", "w+") as json_data:
        json_data.write(file_content)


def update_item_files(items, items_path):
    """
    Updates the item files with their current state as seen in game.
    :param items: dictionary holding the items
    :param items_path: the path to item files
    """
    file_list = [f for f in os.listdir(items_path) if f.endswith(".json")]

    # Clear previous room files
    for f in file_list:
        os.remove(items_path + "/" + f)

    # Create new room files
    for key in items.keys():
        item = items[key]
        create_item_file(item, items_path)


def create_item_file(item, file_path):
    """
    Creates a new json file with the attributes of the given item object.
    :param item: The object we want to convert to a json file
    :param file_path: Where we want to store the new item file
    """
    json_obj = dict()
    json_obj["name"] = item.name
    json_obj["description"] = item.description
    json_obj["actions"] = item.actions
    json_obj["success_message"] = item.success_message
    json_obj["failure_messages"] = item.failure_messages
    json_obj["usable_world"] = item.usable_world
    json_obj["usable_room"] = item.usable_room
    json_obj["num_uses"] = item.num_uses
    json_obj["is_rechargeable"] = item.is_rechargeable
    file_content = json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ': '))

    file_name = convert_to_key(item.name)
    with open(file_path + "/" + file_name + ".json", "w+") as json_data:
        json_data.write(file_content)


def copy_directory(source_path, destination_path):
    """
    Copies the directory from the source path to the destination path.
    :param source_path: The directory we want to copy.
    :param destination_path: Where we want to copy the source.
    """
    copy_tree(source_path, destination_path)


def get_save_files():
    """
    Creates a list of all the save files for Keep Summer Safe
    :return: a list of directory names
    """
    return os.listdir(SAVE_FILE_DIRECTORY_PATH)

