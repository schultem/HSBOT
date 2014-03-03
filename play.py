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
    global NEW_GAME
    NEW_GAME=False
def home():
    global NEW_GAME
    NEW_GAME=False
    logging.info("Clicking PLAY on home screen")
    actions.move_and_leftclick(c(defines.main_menu_play_button))
def play():
    global NEW_GAME
    NEW_GAME=False
    logging.info("Choosing custom decks")
    actions.move_and_leftclick(c(defines.custom_decks_arrow))
    deck = randint(1,defines.DECKS_TO_USE)
    logging.info("Choosing deck %s"%deck)
    actions.move_and_leftclick(c(defines.deck_locations[deck]))
    logging.info("Pressing PLAY on play screen")
    actions.move_and_leftclick(c(defines.play_button))
def queue():
    global NEW_GAME
    NEW_GAME=False
def versus():
    global NEW_GAME
    NEW_GAME=False
def select():
    global NEW_GAME
    NEW_GAME = True
    logging.info("Confirm hand cards")
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
        logging.info("-------------NEW GAME INFO--------------")

    NEW_GAME=False

    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_mids(src,c(defines.player_minions_box),color='green')
    
    logging.info("------PLAY INFO-------")
    logging.info("playable cards:%s"%(str(player_cards)))
    logging.info("player        :%s"%(str(player_attack)))
    logging.info("player ability:%s"%(str(player_ability)))
    logging.info("player minions:%s"%(str(player_minions)))
    logging.info("------PLAY INFO-------")

    logging.info("------PLAY CARDS------")
    play_attempt_counter=0
    while(player_cards != []):
        if play_attempt_counter==3:
            break
        logging.info("attempt to play card:%s"%(str(player_cards[0])))
        logging.info("position_counter:%s play_attempt_counter:%s"%(0,play_attempt_counter))
        actions.leftclick_move_and_leftclick(player_cards[0],[950,600])
        actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(1)
        vision.screen_save()
        src = vision.screen_load()
        player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
        logging.info("playable cards:%s"%(str(player_cards)))
        play_attempt_counter+=1
    logging.info("------PLAY CARDS------")

    logging.info("------PLAY ABILITY------")
    vision.screen_save()
    src = vision.screen_load()
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    if player_ability != [] and player_ability != None:
        logging.info("Use ability")
        actions.move_and_leftclick(c(defines.player_ability))
        actions.move_and_leftclick(c(defines.neutral))
    logging.info("------PLAY ABILITY------")

    logging.info("---ATTACK WITH MINIONS---")
    vision.screen_save()
    src = vision.screen_load()
    previous_player_minions=[]
    player_minions = vision.color_range_mids(src,c(defines.player_minions_box),color='green')
    counter=0
    while player_minions != [] and player_minions != None:
        if previous_player_minions == player_minions:
            if counter==2:
                break
            counter+=1
        logging.info("Attempt to attack with minion %s"%str(player_minions[0]))
        actions.move_and_leftclick(player_minions[0])
        actions.move_cursor([player_minions[0][0],player_minions[0][1]+130])
        logging.info("Get opponent attack info")
        vision.screen_save()
        src = vision.screen_load()
        enemy         = vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box),color='red')
        enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
        logging.info("enemy        :%s"%str(enemy))
        logging.info("enemy minions:%s"%str(enemy_minions))
        if enemy != [] and enemy != None:
            actions.move_and_leftclick(enemy[0])
        elif enemy_minions != [] and enemy_minions != None:
            actions.move_and_leftclick(enemy_minions[0])
        actions.move_and_leftclick(c(defines.neutral_minion))
        vision.screen_save()
        src = vision.screen_load()
        previous_player_minions=player_minions
        player_minions = vision.color_range_mids(src,c(defines.player_minions_box),color='green')
        logging.info("player minions:%s"%(str(player_minions)))
    logging.info("---ATTACK WITH MINIONS---")
    
    logging.info("---ATTACK WITH CHARACTER---")
    actions.move_and_leftclick(c(defines.neutral))
    vision.screen_save()
    src = vision.screen_load()
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    if player_attack != [] and player_attack != None:
        logging.info("Attack with player to enemy")
        logging.info("move to player:%s"%player_attack[0])
        actions.move_and_leftclick(player_attack[0])
        actions.move_cursor([player_attack[0][0],player_attack[0][1]+10])
        actions.pause_pensively(0.1)

        logging.info("Get opponent attack info")
        vision.screen_save()
        src = vision.screen_load()
        enemy         = vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box),color='red')
        enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
        logging.info("enemy        :%s"%str(enemy))
        logging.info("enemy minions:%s"%str(enemy_minions))
        if enemy != [] and enemy != None:
            actions.move_and_leftclick(enemy[0])
        elif enemy_minions != [] and enemy_minions != None:
            actions.move_and_leftclick(enemy_minions[0])
        actions.move_and_leftclick(c(defines.neutral))
    logging.info("---ATTACK WITH CHARACTER---")
    
    logging.info("------PLAY INFO CHECK-------")
    vision.screen_save()
    src = vision.screen_load()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_mids(src,c(defines.player_minions_box),color='green')
    logging.info("playable cards:%s"%(str(player_cards)))
    logging.info("player ability:%s"%(str(player_ability)))
    logging.info("player minions:%s"%(str(player_minions)))
    logging.info("------PLAY INFO CHECK-------")

    if (player_cards==[] and player_ability ==[] and player_minions ==[]) or player_cards==None or player_ability == None or player_minions == None:
        logging.info("---END TURN---")
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.neutral))
        actions.move_and_leftclick(c(defines.turn_button))
        actions.move_and_leftclick(c(defines.neutral))
        logging.info("---END TURN---")

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
    logging.basicConfig(filename='game.log',level=logging.DEBUG)
    logging.info("####################################")
    logging.info("#          NEW SESSION             #")
    logging.info("####################################")

    while(True):
        vision.screen_save()
        src = vision.screen_load()
        new_state = defines.state_dict[vision.get_state(src)]
        logging.info("-------------------------")
        logging.info("STATE | OLD:%s | NEW:%s |"%(old_state,new_state))
        logging.info("-------------------------")
        
        if new_state == old_state and new_state == defines.State.PLAY:
            #Might have been a connection error.
            actions.move_and_leftclick(c(defines.error));
            actions.move_and_leftclick(c(defines.neutral));
        
        states[new_state]()
        if new_state != defines.State.DESKTOP:
            actions.move_and_leftclick(c(defines.neutral));
        actions.pause_pensively(0.1)
        old_state=new_state

if __name__ == '__main__':
    main()

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
#print "player minions    : ",vision.color_range_mids(src,defines.player_minions_box,color='green')
#print "enemy             : ",vision.color_range_reduced_mids(src,defines.reduced_opponent_box,color='red')
#print "enemy minions     : ",vision.color_range_reduced_mids(src,defines.reduced_enemy_minions_box,color='red')
