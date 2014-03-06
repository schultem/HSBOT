import vision
import actions
import defines
import logging
from random import randint
import os

src = None

###############
#    FLAGS    #
###############
NEW_GAME = False

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
    global src
    global NEW_GAME
    
    if NEW_GAME:
        logging.info("-------------NEW GAME INFO--------------")
        logging.info("OPPONENT: %s"%(vision.get_image_info('character',src,c(defines.enemy_box))))
        logging.info("PLAYER  : %s"%(vision.get_image_info('character',src,c(defines.player_box))))
        logging.info("STAGE   : %s"%(vision.get_image_info('stage',src,c(defines.stage_box))))

    NEW_GAME=False
    actions.pause_pensively(1)
    
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',threshold=45)
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))

    #logging.info("------PLAY CARDS------")
    play_attempt_counter=0
    while(player_cards != []):
        if play_attempt_counter==2:
            break
        actions.leftclick_move_and_leftclick(player_cards[0],c(defines.play_card_mid))
        actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(1)
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
    attack_attempt=0 #don't try to attack more than three times with the same minion
    while player_minions != [] and player_minions != None:
        if previous_player_minions == player_minions:
            if attack_attempt==2:
                break
            attack_attempt+=1
        actions.move_and_leftclick(player_minions[0])
        actions.move_cursor([player_minions[0][0],player_minions[0][1]+130])
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
        actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(0.35)
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

    if (player_cards==[] and player_ability ==[] and player_minions ==[]) or player_cards==None or player_ability == None or player_minions == None or attack_attempt == 2:
        #logging.info("---END TURN---")
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.neutral))

def opponent():
    global NEW_GAME
    NEW_GAME=False
def victory():
    global NEW_GAME
    NEW_GAME=False
    logging.info("Victory: Clicking to skip end game results")
    actions.move_and_leftclick(c(defines.neutral))
def defeat():
    global NEW_GAME
    NEW_GAME=False
    logging.info("Defeat: Clicking to skip end game results")
    actions.move_and_leftclick(c(defines.neutral))
def error():
    global NEW_GAME
    NEW_GAME=False
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
    global src
    global NEW_GAME
    new_state=0
    old_state=0
    sigs = vision.get_sigs(os.getcwd()+ '\\images\\state\\')

    logging.basicConfig(filename='game.log',level=logging.DEBUG)
    logging.info("####################################")
    logging.info("#          NEW SESSION             #")
    logging.info("####################################")

    desktop_counter = 0
    while(True):
        src = vision.screen_cap()

        new_state = defines.state_dict[vision.get_state(src,sigs)]        
        if new_state == old_state and new_state == defines.State.PLAY:
            #Might have been a connection error.
            actions.move_and_leftclick(c(defines.error));
            actions.move_and_leftclick(c(defines.neutral));

        states[new_state]()
        if new_state != defines.State.DESKTOP:
            desktop_counter =0
            actions.move_and_leftclick(c(defines.neutral));
        else:
            #on the desktop for some reason, try to start the game going again
            desktop_counter +=1
            actions.pause_pensively(10)
            actions.move_and_leftclick(c(defines.hs_startbar_icon));
            if desktop_counter == 3:
                actions.move_and_leftclick(c(defines.blizzard_startbar_icon));
                actions.move_and_leftclick(c(defines.blizzard_hs_play_button));
                desktop_counter =0
        old_state=new_state

if __name__ == '__main__':
    main()

#src = vision.screen_cap()
#
#vision.screen_save()
#src = vision.screen_load()
#src = vision.imread(os.getcwd() + '\\temp\\attack3.png')
#print defines.enemy_box
#print defines.convert(defines.enemy_box,defines.ref)
#print "game state        : ",defines.state_dict[vision.get_state(src)]
#print "opponent char     : ",vision.get_image_info('character',src,defines.enemy_box)
#print "player char       : ",vision.get_image_info('character',src,defines.player_box)
#print "stage             : ",vision.get_image_info('stage',src,defines.stage_box)
#print "turn              : ",vision.get_image_info('turn',src,defines.turn_box)
#print "playable cards    : ",vision.get_playable_cards(src,defines.hand_box)
#print "player            : ",vision.color_range_reduced_mids(src,defines.reduced_player_box,color='green')
#print "player ability    : ",vision.color_range_reduced_mids(src,defines.reduced_ability_box,color='green')
#print "player minions    : ",player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',threshold=45)
#print "enemy             : ",vision.color_range_reduced_mids(src,defines.reduced_opponent_box,color='red')
#print "enemy minions     : ",vision.color_range_reduced_mids(src,defines.reduced_enemy_minions_box,color='red')
