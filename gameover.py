#!/usr/bin/env python


def check_for_ending(parser):
    """
        Check the defined game ending conditions, and call the appropriate ending.
    """
    if check_win(parser):
        ending = 'win'
    elif check_stranded(parser):
        ending = 'stranded'
    #elif check_death_gravity_boots(parser):
    #    ending = 'death'
    elif check_death_ray_gun(parser):
        ending = 'death'
    else:
        ending = ''
    return ending


def check_win(parser):
    win = False
    if (parser.player.current_room.name == "Summer's Cell") and ("win_flag" in parser.player.current_room.items):
        win = True
    return win


def check_stranded(parser):
    stranded = True
    if parser.items["portal_gun"].num_uses == 0:      # if portal gun charge done, we might be stranded
        for key in parser.player.current_world.rooms.keys():
            room = parser.player.current_world.rooms[key]

            for item_key in room.items:
                if item_key == 'multiverse_battery':
                    stranded = False
                    break
            for hidden_item_key in room.hidden_items:
                if hidden_item_key == 'multiverse_battery':
                    stranded = False
                    break
            for item_key in parser.player.inventory:
                if item_key == 'multiverse_battery':
                    stranded = False
                    break

    else:
        stranded = False
    return stranded

"""
def check_death_gravity_boots(parser):
    death = False
    if (parser.lastcmd == 'use gravity boots' or parser.lastcmd == 'wear gravity boots'
        or parser.lastcmd == 'equip gravity boots' or parser.lastcmd == 'strap gravity boots') and \
            (parser.items["gravity_boots"].num_uses <= 0):
        death = True
    return death
"""

def check_death_ray_gun(parser):
    death = False
    if (parser.lastcmd == 'use ray gun' or parser.lastcmd == 'shoot ray gun'
            or parser.lastcmd == 'fire ray gun') and parser.current_room.name.lower() == "prison entrance":
        death = True
    return death
