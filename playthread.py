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
#logging.basicConfig(filename='game.txt',level=logging.DEBUG)

#Store screen captures
src = None

#pre-calulate sift descriptors
state_descs     = vision.get_descs(os.getcwd()+ '\\images\\state\\')
character_descs = vision.get_descs(os.getcwd()+ '\\images\\character\\')
stage_descs     = vision.get_descs(os.getcwd()+ '\\images\\stage\\')
opponent_char=None
player_char=None
stage=None
current_decknum=None

#get monitor resolution
monitor_x=actions.win32api.GetSystemMetrics(0)
monitor_y=actions.win32api.GetSystemMetrics(1)
defines.screen_box = (0,0,monitor_x,monitor_y)

#Shorter binding for the coord resolution convert function
def c(var):
    return defines.convert(var,defines.ref)

#Update monitor resolution and game screen location and resolution
def update_resolutions():
    logging.info("[ENTER] update_resolutions")
    client_box              = actions.get_client_box("Hearthstone")
    defines.origin          = [client_box[0],client_box[1]]
    defines.game_screen_res = [client_box[2]-client_box[0],client_box[3]-client_box[1]]

#Flags
NEW_GAME     = False
THE_COIN     = True

def desktop():
    logging.info("[ENTER] desktop")
def home():
    logging.info("[ENTER] home")
    control_success=actions.move_and_leftclick(c(defines.main_menu_play_button))
def play():
    global stage_char,player_char,current_decknum
    logging.info("[ENTER] play")
    stage_char=None
    player_char=None
    src = vision.screen_cap()
    read_box = c(defines.state_box[defines.State.PLAY])
    data = vision.read_white_text(src,read_box)
    if 'Play' in data:
        if len(defines.DECKS_TO_USE):
            control_success=actions.move_and_leftclick(c(defines.custom_decks_arrow))
            if defines.PLAY_RANKED:
                control_success=actions.move_and_leftclick(c(defines.ranked_button))
            else:
                control_success=actions.move_and_leftclick(c(defines.casual_button))
            current_decknum=defines.DECKS_TO_USE[randint(0,len(defines.DECKS_TO_USE)-1)]
            control_success=actions.move_and_leftclick(c(defines.deck_locations[current_decknum]))
            control_success=actions.move_and_leftclick(c(defines.play_button))
            actions.pause_pensively(0.5)
def queue():
    logging.info("[ENTER] queue")
    actions.pause_pensively(0.5)
def versus():
    logging.info("[ENTER] versus")
    control_success=actions.move_and_leftclick(c(defines.neutral))
    actions.pause_pensively(10)
def select():
    global NEW_GAME,THE_COIN
    logging.info("[ENTER] select")
    NEW_GAME = True

    if defines.MULLIGAN:
        src = vision.screen_cap()
        choose_3=[]
        choose_4=[]
        for box in defines.starting_hand_costs_3:
            choose_3.append(vision.read_white_data(src,c(box)))
        for box in defines.starting_hand_costs_4:
            choose_4.append(vision.read_white_data(src,c(box)))
        #print choose_3
        #print choose_4
        return_list=[]
        if '' not in choose_3:
            THE_COIN=False
            for choice in range(0,len(choose_3)):
                if int(choose_3[choice]) >= 4:
                    coord=defines.starting_hand_costs_3[choice]
                    return_list.append([coord[2],coord[3]])#return the lower right of the detection box which is over the card to click on
        elif '' not in choose_4:
            THE_COIN=True
            for choice in range(0,len(choose_4)):
                if int(choose_4[choice]) >= 5:
                    coord=defines.starting_hand_costs_4[choice]
                    return_list.append([coord[2],coord[3]])#return the lower right of the detection box which is over the card to click on
                if int(choose_4[choice]) == 1:
                    coord=defines.starting_hand_costs_4[choice]
                    return_list.append([coord[2],coord[3]])#return the lower right of the detection box which is over the card to click on
        for coord in return_list:
            control_success=actions.move_and_leftclick(c(coord))

    control_success=actions.move_and_leftclick(c(defines.confirm_hand_button))
    control_success=actions.move_and_leftclick(c(defines.neutral))
def wait():
    logging.info("[ENTER] wait")
def player():
    global src
    global NEW_GAME,opponent_char,player_char,stage,current_decknum
    logging.info("[ENTER] player")
    control_success=True#keep track of whether or not the bot was able to control the mouse.  If not the user is attempting to use it
    actions.pause_pensively(1)

    if NEW_GAME:
        src = vision.screen_cap()
        stage=vision.get_image_info_sift(src,stage_descs,c(defines.stage_box))
        NEW_GAME=False

    #logging.info("------GET MATCH INFO------")
    src = vision.screen_cap()
    if player_char==None:
        try:
            player_char=vision.get_image_info_sift(src,character_descs,c(defines.player_box))
        except:
            player_char=None
    if stage==None:
        try:
            stage=vision.get_image_info_sift(src,stage_descs,c(defines.stage_box))
        except:
            stage=None

    #logging.info("------PLAY CARDS------")
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    while player_cards and control_success:
        if current_decknum != None:
            if defines.TARGETING[current_decknum]:
                control_success=actions.move_and_leftclick(player_cards[0])
                actions.move_cursor(c(defines.nuetral_targeting))
                src = vision.screen_cap()
                targeting = vision.color_range_reduced_mids(src,c(defines.nuetral_targeting_box),color='red_targeting')
                if targeting:
                    if defines.TARGETING[current_decknum]==defines.Target.OPPONENT_HERO:
                        control_success=actions.move_and_leftclick(c(defines.opponent_hero))
                if defines.TARGETING[current_decknum]==defines.Target.OPPONENT_HERO:
                    actions.move_and_leftclick(c(defines.play_card[randint(0,len(defines.play_card)-1)]))
                    actions.move_cursor(c(defines.nuetral_targeting))
                    src = vision.screen_cap()
                    targeting = vision.color_range_reduced_mids(src,c(defines.nuetral_targeting_box),color='red_targeting')
                    if targeting:
                        if defines.TARGETING[current_decknum]==defines.Target.OPPONENT_HERO:
                            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
            else:
                actions.leftclick_move_and_leftclick(player_cards[0],c(defines.play_card[randint(0,len(defines.play_card)-1)]))
        else:
            actions.leftclick_move_and_leftclick(player_cards[0],c(defines.play_card[randint(0,len(defines.play_card)-1)]))
        control_success=actions.move_and_rightclick(c(defines.neutral_minion))
        actions.pause_pensively(1.5)
        src = vision.screen_cap()
        player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
        if not actions.check_game('Hearthstone'):
            break

    #logging.info("------PLAY ABILITY------")
    actions.pause_pensively(0.50)
    src = vision.screen_cap()
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    if player_ability and player_char and control_success:
        if player_char == 'mage':
            control_success=actions.move_and_leftclick(c(defines.player_ability))
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
        elif player_char == 'priest':
            control_success=actions.move_and_leftclick(c(defines.player_ability))
            control_success=actions.move_and_leftclick(c(defines.player_hero))
        else:
            control_success=actions.move_and_leftclick(c(defines.player_ability))
            control_success=actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(2)


    #logging.info("---ATTACK WITH MINIONS---")
    src = vision.screen_cap()
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)
    while player_minions and control_success:
        p_m=False
        no_enemy_taunts_detected=True
        min_subset = [False,99]
        src = vision.screen_cap()
        enemy_minions = vision.get_taunt_minions(src,c(defines.enemy_minions_box_taunts))

        if enemy_minions:
            no_enemy_taunts_detected=False
            if defines.RANDOM_ATTACKS:
                p_m = player_minions[randint(0,len(player_minions)-1)] #attack with a random minion
                e_m = enemy_minions[randint(0,len(enemy_minions)-1)] #attack a random taunt minion
            else:
                if control_success:
                    player_minions_data = vision.all_minion_data(src,defines.player_minion_data_split,defines.c(defines.player_minions_box),minions_box_playable=defines.c(defines.reduced_player_minions_box),stage=stage)
                    enemy_minions_data  = vision.all_minion_data(src,defines.enemy_minion_data_split,defines.c(defines.enemy_minions_box),minions_box_taunts_reduced=c(defines.reduced_enemy_minions_box),minions_box_taunts=defines.c(defines.enemy_minions_box_taunts),stage=stage,reduced_color='red')
                    print ''
                    for i in range(0,len(enemy_minions_data)):
                        print enemy_minions_data[i]
                    print ""
                    for i in range(0,len(player_minions_data)):
                        print player_minions_data[i]
                        
                    playable_minions=[]
                    for player_minion in player_minions_data:
                        if player_minion['playable'] == True:
                            playable_minions.append(player_minion)
                    if playable_minions==[]:
                        break

                    taunt_minions = []
                    for enemy_minion in enemy_minions_data:
                        if enemy_minion['taunt'] == True:
                            taunt_minions.append(enemy_minion)
                    subsets=[]
                    for L in range(0,len(playable_minions)+1):
                        for subset in combinations(playable_minions,L):
                            attack_total=0
                            for individual in subset:
                                if 'attack' in individual:
                                    if individual['attack'] != ' ':
                                        attack_total+=int(individual['attack'])
                            if subset:
                                subsets.append([subset,attack_total])

                    min_subset = [False,99]
                    #max_taunt  = 0
                    min_difference = 99
                    for taunt_minion in taunt_minions:
                        #if taunt_minion['defense']>max_taunt[0]:
                        #    max_taunt=taunt_minion['defense']

                        if 'defense' in taunt_minion:
                            if taunt_minion['defense']==' ':
                                taunt_minion['defense']='5'
                        else:
                            taunt_minion['defense']='5'

                        for subset in subsets:
                            difference = abs(subset[1]-int(taunt_minion['defense']))
                            if subset[1]>=taunt_minion['defense'] and difference<min_difference and (subset[1]<min_subset[1] or len(subset)<len(min_subset)):#attack_total > taunt defense
                                min_subset=subset
                                min_difference=difference
                                p_m = min_subset[0][0]['coord']
                                e_m = taunt_minion['coord']

                    if p_m == False:
                        p_m = player_minions[randint(0,len(player_minions)-1)] #attack with a random minion
                        e_m = enemy_minions[randint(0,len(enemy_minions)-1)] #attack a random taunt minion
                    print 'Use subset: ',min_subset
        else:
            no_enemy_taunts_detected=True
            p_m = player_minions[0] #default attack with the leftmost minion if there are no taunts

        control_success=actions.move_and_leftclick(p_m)
        actions.move_cursor([p_m[0],p_m[1]+int(150*float(defines.game_screen_res[1])/float(defines.ref_game_screen_res[1]))])
        actions.pause_pensively(0.2)

        src = vision.screen_cap()
        enemy=[]
        enemy_freeze=None
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box1),color='red'))
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box2),color='red'))
        enemy_freeze = vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box1),color='blue')
        enemy_minions = vision.get_taunt_minions(src,c(defines.enemy_minions_box_taunts))
        if enemy_minions and no_enemy_taunts_detected:#something wrong has happened, try a bunch of stuff
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
            actions.pause_pensively(2)
            control_success=actions.move_and_leftclick(p_m)
            actions.move_cursor([p_m[0],p_m[1]+int(150*float(defines.game_screen_res[1])/float(defines.ref_game_screen_res[1]))])
            actions.pause_pensively(0.2)
            e_m = enemy_minions[randint(0,len(enemy_minions)-1)] #attack a random taunt minion
            control_success=actions.move_and_leftclick(e_m)
            actions.pause_pensively(2.5)
        elif enemy_minions:
            control_success=actions.move_and_leftclick(e_m)
            actions.pause_pensively(2.5)
        elif enemy:
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
        elif enemy_freeze:
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
        else:
            #something's wrong, try to attack any minion
            actions.pause_pensively(6)
            enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
            if enemy_minions:
                e_m = enemy_minions[randint(0,len(enemy_minions)-1)] #attack a random taunt minion
                control_success=actions.move_and_leftclick(e_m)
                actions.pause_pensively(2.5)
            else:
                actions.pause_pensively(6)
        control_success=actions.move_and_rightclick(c(defines.neutral_minion))
        src = vision.screen_cap()
        state_name = vision.get_state_sift(src,state_descs,ignore_list=['versus.png','defeat.png','finding_opponent.png','gold.png','opponent_still_choosing.png','starting_hand.png','rank.png','victory.png'])
        if state_name == 'play':
            break
        if not actions.check_game('Hearthstone'):
            break
        player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)

    #logging.info("---ATTACK WITH CHARACTER---")
    actions.pause_pensively(0.25)
    src = vision.screen_cap()
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    if player_attack and control_success:
        control_success=actions.move_and_leftclick(c(defines.neutral_minion))
        control_success=actions.move_and_leftclick(player_attack[0])
        actions.move_cursor([player_attack[0][0],player_attack[0][1]+10])
        actions.pause_pensively(0.1)
        src = vision.screen_cap()
        enemy=[]
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box1),color='red'))
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box2),color='red'))
        enemy_minions = vision.get_taunt_minions(src,c(defines.enemy_minions_box_taunts))
        if enemy_minions:
            e_m = randint(0,len(enemy_minions)-1) #attack a random taunt minion

        if enemy_minions:
            control_success=actions.move_and_leftclick(enemy_minions[e_m])
        elif enemy:
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
        else:
            #something's wrong, try to attack any minion
            actions.pause_pensively(6)
            enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
            if enemy_minions:
                control_success=actions.move_and_leftclick(enemy_minions[0])
        control_success=actions.move_and_leftclick(c(defines.neutral))

    #logging.info("------PLAY INFO CHECK-------")
    actions.pause_pensively(0.25)
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    if (player_cards==[] and player_ability ==[] and player_minions ==[] and player_attack ==[]) or player_cards==None or player_ability == None or player_minions == None or player_attack==None and control_success:
        #logging.info("---END TURN---")
        control_success=actions.move_and_leftclick(c(defines.neutral))
        player_turn_green_check = vision.color_range_reduced_mids(src,c(defines.turn_box),color='green')
        if player_turn_green_check !=[] and player_turn_green_check != None and control_success:
            control_success=actions.move_and_leftclick(c(defines.turn_button))
            control_success=actions.move_and_leftclick(c(defines.turn_button))
            control_success=actions.move_and_leftclick(c(defines.neutral))
        else:
            actions.pause_pensively(5)
            player_end()

def opponent():
    logging.info("[ENTER] opponent")
def victory():
    logging.info("[ENTER] victory")
    control_success=actions.move_and_leftclick(c(defines.neutral))
def defeat():
    logging.info("[ENTER] defeat")
    control_success=actions.move_and_leftclick(c(defines.neutral))
def error():
    logging.info("[ENTER] error")
    control_success=actions.move_and_leftclick(c(defines.error))
def rank():
    logging.info("[ENTER] rank")
    control_success=actions.move_and_leftclick(c(defines.neutral))
    control_success=actions.move_and_leftclick(c(defines.main_screen_splash))
def player_end():
    global src#,character_descs,stage_descs
    global NEW_GAME,opponent_char,player_char

    logging.info("[ENTER] player_end")
    control_success=actions.move_and_leftclick(c(defines.neutral))
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=37,max_threshold=200)
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    if (player_cards==[] and player_ability ==[] and player_minions ==[] and player_attack ==[]) and control_success:
        #logging.info("---END TURN---")
        control_success=actions.move_and_leftclick(c(defines.turn_button))
        control_success=actions.move_and_leftclick(c(defines.neutral))

states = {
    defines.State.DESKTOP       :desktop,
    defines.State.HOME          :home,
    defines.State.PLAY          :play,
    defines.State.QUEUE         :queue,
    defines.State.VERSUS        :versus,
    defines.State.SELECT        :select,
    defines.State.WAIT          :wait,
    defines.State.PLAYER        :player,
    defines.State.OPPONENT      :opponent,
    defines.State.VICTORY       :victory,
    defines.State.DEFEAT        :defeat,
    defines.State.ERROR         :error,
    defines.State.RANK          :rank,
    defines.State.PLAYER_GREEN  :player_end,
}

class GameLogicThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self._stop = threading.Event()
        self.new_state=0
        self.old_state=0
        self.state_desc = {
                      0:'starting game',
                      1:'home screen',
                      2:'select deck',
                      3:'finding opponent',
                      4:'versus',
                      5:'exchange cards',
                      6:'waiting',
                      7:'bot turn',
                      8:'opponent turn',
                      9:'waiting',
                      10:'waiting',
                      11:'error',
                      12:'rank',
                      13:'end bot turn'
                     }
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.new_state=0
        self.old_state=0
        self.queue.put("Starting bot")
        wait_count=0
        previous_hour=0
        wait_for_start_time=True
        while(not self.stopped()):
            current_hour = int(strftime("%X")[:2])
            if current_hour==0:
                current_hour=24

            if current_hour==defines.STOP_HOUR and defines.STOP_HOUR!=0 and (self.new_state == defines.State.PLAY or self.new_state == defines.State.HOME):
                if defines.STOP_HOUR >= 12 and defines.STOP_HOUR != 24:
                    am_or_pm='pm'
                else:
                    am_or_pm='am'
                time_to_stop = defines.STOP_HOUR%12
                if time_to_stop==0:
                    time_to_stop=12

                wait_for_start_time=True
                self.queue.put("stopped at %s o'clock %s"%(time_to_stop,am_or_pm))

            if not wait_for_start_time:
                #check if battle net is running and Hearthstone is running and shown
                if actions.check_bnet("Battle.net"):
                    if actions.check_game("Hearthstone") == False:
                        self.new_state=defines.State.DESKTOP
                    else:
                        update_resolutions()
                        try:
                            src = vision.screen_cap()
                            
                            state_name = vision.get_state_sift(src,state_descs)
                            if state_name != None:
                                self.new_state  = defines.state_dict[state_name]
                            else:
                                self.new_state=defines.State.DESKTOP
                            
                            if self.new_state == self.old_state and (self.new_state == defines.State.PLAY or self.new_state == defines.State.HOME):
                                #Might have been a connection error.
                                self.queue.put("Must enable at least one custom deck in Options!")
                                control_success=actions.move_and_leftclick(c(defines.error))
                                control_success=actions.move_and_leftclick(c(defines.neutral))
                            
                            #if self.new_state == defines.State.PLAY and self.old_state == defines.State.QUEUE:
                            #    self.new_state = defines.State.QUEUE
                    
                        except:
                            self.queue.put("Error: Invalid state, starting the bot again may help")
                            self.stop()
                else:
                    self.queue.put("Error: Battle.net may not be running, please start Battle.net")
                    self.stop()
                  
                #check and reroll 40 gold quests once per day at reroll time
                if defines.REROLL_QUESTS:
                    time_str = strftime("%X", gmtime())
                    if int(time_str[:2])!=previous_hour and (self.new_state==defines.State.HOME or self.new_state==defines.State.PLAY) and not self.stopped():
                        self.queue.put('checking quests')
                        if self.new_state==defines.State.PLAY:
                            control_success=actions.move_and_leftclick(c(defines.play_back_button))
                            actions.pause_pensively(2)
                        control_success=actions.move_and_leftclick(c(defines.quest_button))
                        actions.pause_pensively(2)
                        src = vision.screen_cap()
                        
                        if '40' in vision.read_white_data(src,c(defines.quest_box_1)):
                            #vision.imwrite('reroll_before.png',src)
                            control_success=actions.move_and_leftclick(c(defines.reroll_quest_button_1))
                            #vision.imwrite('reroll_after.png',src)
                        if '40' in vision.read_white_data(src,c(defines.quest_box_2)):
                            control_success=actions.move_and_leftclick(c(defines.reroll_quest_button_2))
                        if '40' in vision.read_white_data(src,c(defines.quest_box_3)):
                            control_success=actions.move_and_leftclick(c(defines.reroll_quest_button_3))
                        control_success=actions.move_and_leftclick(c(defines.main_menu_nuetral))
                        self.new_state=defines.State.HOME
                        previous_hour=int(time_str[:2])
                        src = vision.screen_cap()
                
                self.queue.put(self.state_desc[self.new_state])
                
                #check if waiting for a long time, try clicking just in case
                if self.state_desc[self.new_state]=='waiting':
                    if wait_count >= 5:
                        control_success=actions.move_and_leftclick(c(defines.neutral))
                        wait_count=0
                    else:
                        wait_count+=1
                
                if self.new_state != defines.State.DESKTOP and not self.stopped():
                    states[self.new_state]()
                elif self.new_state == defines.State.DESKTOP and not self.stopped():
                    #on the desktop for some reason, try to start the game or reshow the window if it's already running
                    actions.pause_pensively(5)
                    if not self.stopped():
                        actions.restart_game()
                        update_resolutions()
                        control_success=actions.move_and_leftclick(c(defines.neutral))
                self.old_state=self.new_state
            else:
                if defines.START_HOUR >= 12 and defines.START_HOUR != 24:
                    am_or_pm='pm'
                else:
                    am_or_pm='am'
                time_to_start = defines.START_HOUR%12
                if time_to_start==0:
                    time_to_start=12
                current_hour = int(strftime("%X")[:2])
                if current_hour==0:
                    current_hour=24
                if defines.START_HOUR==current_hour or defines.START_HOUR==0:
                    wait_for_start_time=False
                else:
                    self.queue.put("waiting for %s o'clock %s"%(time_to_start,am_or_pm))
                    actions.pause_pensively(1)
