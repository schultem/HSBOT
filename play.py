import vision
import actions
import defines
import logging
from random import randint
import os

src = None
state_sigs = None
character_sigs = None
stage_sigs = None
state_descs = None
character_descs = None
stage_descs = None
opponent_char=None
player_char=None

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
    actions.move_and_leftclick(c(defines.deck_locations[defines.DECKS_TO_USE[randint(0,len(defines.DECKS_TO_USE)-1)]]))
    actions.move_and_leftclick(c(defines.play_button))
    actions.pause_pensively(3)
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
    global src,character_descs
    global NEW_GAME,opponent_char,player_char
    actions.pause_pensively(1)

    if NEW_GAME:
        logging.info("-------------NEW GAME INFO--------------")
        opponent_char=vision.get_image_info_sift(src,character_descs,c(defines.enemy_box))
        logging.info("OPPONENT: %s"%(opponent_char))
        player_char=vision.get_image_info_sift(src,character_descs,c(defines.player_box))
        logging.info("PLAYER:   %s"%(player_char))
        #logging.info("STAGE:    %s"%(vision.get_image_info_sift(src,stage_descs,c(defines.stage_box))))
        NEW_GAME=False

    #logging.info("------PLAY CARDS------")
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    while(player_cards != []):

        actions.leftclick_move_and_leftclick(player_cards[0],c(defines.play_card[randint(0,1)]))
        actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(1.5)
        src = vision.screen_cap()
        player_cards   = vision.get_playable_cards(src,c(defines.hand_box))

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
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)
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
        player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)
    
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
    actions.pause_pensively(1)
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)

    if (player_cards==[] and player_ability ==[] and player_minions ==[]) or player_cards==None or player_ability == None or player_minions == None:
        #logging.info("---END TURN---")
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.neutral))

def opponent():
    pass
def victory():
    actions.pause_pensively(1)
    #verify the state
    src = vision.screen_cap()
    new_state  = defines.state_dict[vision.get_state_sift(src,state_descs)]
    if new_state != None and new_state == defines.State.VICTORY:
        logging.info("Victory")
        actions.move_and_leftclick(c(defines.neutral))
def defeat():
    actions.pause_pensively(1)
    #verify the state
    src = vision.screen_cap()
    new_state  = defines.state_dict[vision.get_state_sift(src,state_descs)]
    if new_state != None and new_state == defines.State.DEFEAT:
        logging.info("Defeat")
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

#Update monitor resolution and game screen location and resolution
def update_resolutions():
    monitor_x=actions.win32api.GetSystemMetrics(0)
    monitor_y=actions.win32api.GetSystemMetrics(1)
    defines.screen_box      = (0,0,monitor_x,monitor_y)
    client_box              = actions.get_client_box()
    defines.origin          = [client_box[0],client_box[1]]
    defines.game_screen_res = [client_box[2]-client_box[0],client_box[3]-client_box[1]]

def main():
    global src,character_descs,state_descs,stage_descs
    global NEW_GAME
    new_state=0
    old_state=0
    #get monitor resolution
    monitor_x=actions.win32api.GetSystemMetrics(0)
    monitor_y=actions.win32api.GetSystemMetrics(1)
    defines.screen_box      = (0,0,monitor_x,monitor_y)

    state_descs     = vision.get_descs(os.getcwd()+ '\\images\\state\\')
    character_descs = vision.get_descs(os.getcwd()+ '\\images\\character\\')
    #stage_descs = vision.get_descs(os.getcwd()+ '\\images\\stage\\')
    
    logging.basicConfig(filename='game.log',level=logging.DEBUG)
    
    while(True):
        src = vision.screen_cap()
        
        state_name = vision.get_state_sift(src,state_descs)
        if state_name != None:
            new_state  = defines.state_dict[state_name]
        else:
            new_state=defines.State.DESKTOP
        
        if new_state == old_state and new_state == defines.State.PLAY:
            #Might have been a connection error.
            actions.move_and_leftclick(c(defines.error))
            actions.move_and_leftclick(c(defines.neutral))
        
        #check if Hearthstone is running and shown
        if actions.check_game() == False:
            new_state=defines.State.DESKTOP
        else:
            update_resolutions()

        if new_state != defines.State.DESKTOP:
            states[new_state]()
        else:
            #on the desktop for some reason, try to start the game or reshow the window if it's already running
            actions.pause_pensively(10)
            actions.restart_game()
            update_resolutions()
            actions.move_and_leftclick(c(defines.neutral))
        old_state=new_state

if __name__ == '__main__':
    main()