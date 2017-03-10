#!/usr/bin/env python
import parser

def check_for_ending(parser):

    if check_stranded(parser):
        ending = 'stranded'
    else:
        ending = ''

    return ending

def check_stranded(parser):
    stranded = True
    if (parser.items["portal_gun"].num_uses == 0):      # if portal gun charge done, we might be stranded
        for key in parser.player.current_world.rooms.keys():
            room = parser.player.current_world.rooms[key]

            for item_key in room.items:
                if item_key == 'battery':
                    stranded = False
                    break
            for hidden_item_key in room.hidden_items:
                if hidden_item_key == 'battery':
                    stranded = False
                    break
            for item_key in parser.player.inventory:
                if item_key == 'battery':
                    stranded = False
                    break

    else:
        stranded = False
    return stranded
