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

#Store screen captures
src = None

def main():
    global src
    #defines.game_screen_res = [1366,768]
    box  = defines.c(defines.player_minion_data)

    src = vision.imread('temp.png')
    #print vision.get_taunt_minions(src,box)
    print vision.read_card_data(src,box)

if __name__ == '__main__':
    main()