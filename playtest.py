import vision
import actions
import defines
import logging
from random import randint
import os
from Tkinter import *
import tkFont
import threading
import Queue
import base64
import qr

#pre-calulate sift descriptors
#state_descs     = vision.get_descs(os.getcwd()+ '\\images\\state\\')
#character_descs = vision.get_descs(os.getcwd()+ '\\images\\character\\')
#stage_descs     = vision.get_descs(os.getcwd()+ '\\images\\stage\\')
opponent_char=None
player_char=None
stage=None

#Store screen captures
src = None

def main():
    global src
    #defines.game_screen_res = [1366,768]

    #print vision.read_card_data(src)
    src = vision.imread('2taunt.png')

    stage='china'
    enemy_minions = vision.all_minion_data(src,defines.c(defines.enemy_minion_data),defines.c(defines.enemy_minions_box),minions_box_taunts=defines.c(defines.enemy_minions_box_taunts),stage=stage)
    print enemy_minions
    print ""
    player_minions = vision.all_minion_data(src,defines.c(defines.player_minion_data),defines.c(defines.player_minions_box),minions_box_playable=defines.c(defines.reduced_player_minions_box),stage=stage)
    for i in range(0,len(player_minions)):
        print player_minions[i]

if __name__ == '__main__':
    main()