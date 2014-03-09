import vision
import actions
import defines
import logging
from random import randint
import os
import win32gui
import win32con

src = None
state_sigs = None
character_sigs = None
stage_sigs = None

###############
#    FLAGS    #
###############
NEW_GAME = False
THE_COIN = False

def desktop():
    pass
def home():
    actions.move_and_leftclick(c(defines.main_menu_play_button))
def play():
    actions.move_and_leftclick(c(defines.custom_decks_arrow))
    actions.move_and_leftclick(defines.deck_locations[defines.DECKS_TO_USE[randint(0,len(defines.DECKS_TO_USE)-1)]])
    actions.move_and_leftclick(c(defines.play_button))
def queue():
    pass
def versus():
    pass
def select():
    global NEW_GAME
    NEW_GAME = True
    
    actions.move_and_leftclick(c(defines.confirm_hand_button))
def wait():
    pass
def player():
    global src,character_sigs,stage_sigs
    global NEW_GAME
    actions.pause_pensively(1)

    if NEW_GAME:
        logging.info("-------------NEW GAME INFO--------------")
        logging.info("OPPONENT: %s"%(vision.get_image_info(src,character_sigs,c(defines.enemy_box))))
        logging.info("PLAYER:   %s"%(vision.get_image_info(src,character_sigs,c(defines.player_box))))
        #logging.info("STAGE:    %s"%(vision.get_image_info(src,stage_sigs,c(defines.stage_box))))
        NEW_GAME=False

    #logging.info("------PLAY CARDS------")
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    play_attempt_counter=0
    while(player_cards != []):
        if play_attempt_counter==2:
            break
        actions.leftclick_move_and_leftclick(player_cards[0],c(defines.play_card[randint(0,1)]))
        actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(1.5)
        src = vision.screen_cap()
        player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
        play_attempt_counter+=1

    #logging.info("------PLAY ABILITY------")
    actions.pause_pensively(0.50)
    src = vision.screen_cap()
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    if player_ability != [] and player_ability != None:
        actions.move_and_leftclick(c(defines.player_ability))
        actions.move_and_leftclick(c(defines.neutral))

    #logging.info("---ATTACK WITH MINIONS---")
    src = vision.screen_cap()
    previous_player_minions=[]
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',threshold=45)
    while player_minions != [] and player_minions != None:
        p_m = randint(0,len(player_minions)-1) #attack with a random minion
        actions.move_and_leftclick(player_minions[p_m])
        actions.move_cursor([player_minions[p_m][0],player_minions[p_m][1]+130])
        actions.pause_pensively(0.35)
        src = vision.screen_cap()
        enemy=[]
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box1),color='red'))
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box2),color='red'))
        enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
        if enemy_minions != []:
            e_m = randint(0,len(enemy_minions)-1) #attack a random taunt minion
        else:
            e_m = []
        if enemy != [] and enemy != None:
            actions.move_and_leftclick(c(defines.opponent_hero))
        elif enemy_minions != [] and enemy_minions != None:
            actions.move_and_leftclick(enemy_minions[e_m])
        else:
            actions.pause_pensively(6)
        actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(0.50)
        src = vision.screen_cap()
        previous_player_minions=player_minions
        player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',threshold=45)
    
    #logging.info("---ATTACK WITH CHARACTER---")
    actions.move_and_leftclick(c(defines.neutral))
    src = vision.screen_cap()
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    if player_attack != [] and player_attack != None:
        actions.move_and_leftclick(player_attack[0])
        actions.move_cursor([player_attack[0][0],player_attack[0][1]+10])
        actions.pause_pensively(0.35)
        src = vision.screen_cap()
        enemy=[]
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box1),color='red'))
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box2),color='red'))
        enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
        if enemy != [] and enemy != None:
            actions.move_and_leftclick(c(defines.opponent_hero))
        elif enemy_minions != [] and enemy_minions != None:
            actions.move_and_leftclick(enemy_minions[0])
        actions.move_and_leftclick(c(defines.neutral))
    
    #logging.info("------PLAY INFO CHECK-------")
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',threshold=45)

    if (player_cards==[] and player_ability ==[] and player_minions ==[]) or player_cards==None or player_ability == None or player_minions == None:
        #logging.info("---END TURN---")
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.neutral))

def opponent():
    pass
def victory():
    logging.info("Victory: Clicking to skip end game results")
    actions.move_and_leftclick(c(defines.neutral))
def defeat():
    logging.info("Defeat: Clicking to skip end game results")
    actions.move_and_leftclick(c(defines.neutral))
def error():
    logging.info("Error: Clicking OK in error message")
    actions.move_and_leftclick(c(defines.error))

states = {
    defines.State.DESKTOP  :desktop,
    defines.State.HOME     :home,
    defines.State.PLAY     :play,
    defines.State.QUEUE    :queue,
    defines.State.VERSUS   :versus,
    defines.State.SELECT   :select,
    defines.State.WAIT     :wait,
    defines.State.PLAYER   :player,
    defines.State.OPPONENT :opponent,
    defines.State.VICTORY  :victory,
    defines.State.DEFEAT   :defeat,
    defines.State.ERROR    :error,
}

def c(var):
    new = var
    return defines.convert(var,defines.ref)

def main():
    global src,character_sigs,state_sigs,stage_sigs
    global NEW_GAME
    new_state=0
    old_state=0
    def _window_callback(hwnd, all_windows):
        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    state_sigs = vision.get_sigs(os.getcwd()+ '\\images\\state\\')
    character_sigs = vision.get_sigs(os.getcwd()+ '\\images\\character\\')
    #stage_sigs = vision.get_sigs(os.getcwd()+ '\\images\\stage\\')

    logging.basicConfig(filename='game.log',level=logging.DEBUG)
    logging.info("####################################")
    logging.info("#          NEW SESSION             #")
    logging.info("####################################")

    desktop_counter = 0
    while(True):
        src = vision.screen_cap()
    
        new_state = defines.state_dict[vision.get_state(src,state_sigs)]    
     
        if new_state == old_state and new_state == defines.State.PLAY:
            #Might have been a connection error.
            actions.move_and_leftclick(c(defines.error));
            actions.move_and_leftclick(c(defines.neutral));
    
        states[new_state]()
        if new_state != defines.State.DESKTOP:
            actions.move_and_leftclick(c(defines.neutral));
        else:
            #on the desktop for some reason, try to start the game or reshow the window if it's already running
            actions.pause_pensively(10)
            hwnd =  win32gui.FindWindow(0, "Hearthstone")
            if hwnd != None and hwnd != 0:
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                actions.pause_pensively(5)
            else:
                actions.move_and_leftclick(c(defines.blizzard_hs_play_button));
                actions.pause_pensively(10)
            
        old_state=new_state

if __name__ == '__main__':
    main()