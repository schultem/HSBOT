import vision
import actions
import defines
import logging
from random import randint
import os
import threading
import Queue
from countdict import countdict
from time import gmtime, strftime
from itertools import combinations

#pre-calulate sift descriptors
#state_descs     = vision.get_descs(os.getcwd()+ '\\images\\state\\')
#character_descs = vision.get_descs(os.getcwd()+ '\\images\\character\\')
#stage_descs     = vision.get_descs(os.getcwd()+ '\\images\\stage\\')
opponent_char=None
player_char=None
stage=None

#Store screen captures
src = None

#Shorter binding for the coord resolution convert function
def c(var):
    return defines.convert(var,defines.ref)

def main():
    global src
    #defines.game_screen_res = [1359,743]
    
    #defines.game_screen_res = [1366,768]
    #defines.origin          = [3,22]
    #defines.screen_box      = [0,0,1920,1080]
    #defines.origin          = [0,0]
    #defines.screen_box      = [0,0,1359,743]
    #src = vision.imread('temp.png')
    #print vision.get_taunt_minions(src,defines.enemy_minions_box_taunts)
    
if __name__ == '__main__':
    main()