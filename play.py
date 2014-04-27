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
from countdict import countdict
from time import gmtime, strftime

#Store screen captures
src = None

#pre-calulate sift descriptors
state_descs     = vision.get_descs(os.getcwd()+ '\\images\\state\\')
character_descs = vision.get_descs(os.getcwd()+ '\\images\\character\\')
stage_descs     = vision.get_descs(os.getcwd()+ '\\images\\stage\\')
opponent_char=None
player_char=None
stage=None

#get monitor resolution
monitor_x=actions.win32api.GetSystemMetrics(0)
monitor_y=actions.win32api.GetSystemMetrics(1)
defines.screen_box = (0,0,monitor_x,monitor_y)

#Shorter binding for the coord resolution convert function
def c(var):
    return defines.convert(var,defines.ref)

#Update monitor resolution and game screen location and resolution
def update_resolutions():
    client_box              = actions.get_client_box("Hearthstone")
    defines.origin          = [client_box[0],client_box[1]]
    defines.game_screen_res = [client_box[2]-client_box[0],client_box[3]-client_box[1]]

#Flags
NEW_GAME     = False
THE_COIN     = True

def desktop():
    pass
def home():
    control_success=actions.move_and_leftclick(c(defines.main_menu_play_button))
def play():
    global stage_char,player_char
    stage_char=None
    player_char=None
    if len(defines.DECKS_TO_USE):
        control_success=actions.move_and_leftclick(c(defines.custom_decks_arrow))
        control_success=actions.move_and_leftclick(c(defines.deck_locations[defines.DECKS_TO_USE[randint(0,len(defines.DECKS_TO_USE)-1)]]))
        control_success=actions.move_and_leftclick(c(defines.play_button))
def queue():
    pass
def versus():
    control_success=actions.move_and_leftclick(c(defines.neutral))
    actions.pause_pensively(10)
def select():
    global NEW_GAME,THE_COIN
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
    pass
def player():
    global src
    global NEW_GAME,opponent_char,player_char,stage
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
    while(player_cards != [] and control_success):
        actions.leftclick_move_and_leftclick(player_cards[0],c(defines.play_card[randint(0,1)]))
        control_success=actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(1.5)
        src = vision.screen_cap()
        player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    actions.pause_pensively(3)

    #logging.info("------PLAY ABILITY------")
    actions.pause_pensively(0.50)
    src = vision.screen_cap()
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    if player_ability != [] and player_ability != None and player_char != None and control_success:
        if player_char == 'mage':
            control_success=actions.move_and_leftclick(c(defines.player_ability))
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
        elif player_char == 'priest':
            control_success=actions.move_and_leftclick(c(defines.player_ability))
            control_success=actions.move_and_leftclick(c(defines.player_hero))
        else:
            control_success=actions.move_and_leftclick(c(defines.player_ability))
            control_success=actions.move_and_leftclick(c(defines.neutral_minion))
        actions.pause_pensively(1)
    #logging.info("---ATTACK WITH MINIONS---")
    src = vision.screen_cap()

    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)
    while player_minions != [] and player_minions != None and control_success:
        p_m = randint(0,len(player_minions)-1) #attack with a random minion
        control_success=actions.move_and_leftclick(player_minions[p_m])
        actions.move_cursor([player_minions[p_m][0],player_minions[p_m][1]+130])
        actions.pause_pensively(0.35)
        src = vision.screen_cap()
        enemy=[]
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box1),color='red'))
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box2),color='red'))
        enemy_minions = vision.get_taunt_minions(src,c(defines.enemy_minions_box_taunts))
        if enemy_minions != []:
            if defines.RANDOM_ATTACKS:
                e_m = randint(0,len(enemy_minions)-1) #attack a random taunt minion
            #else:
            #    if control_success:
            #        print ''
            #        enemy_minions = vision.all_minion_data(src,defines.enemy_minion_data_split,defines.c(defines.enemy_minions_box),minions_box_taunts_reduced=c(defines.reduced_enemy_minions_box),minions_box_taunts=defines.c(defines.enemy_minions_box_taunts),stage=stage,reduced_color='red')
            #        for i in range(0,len(enemy_minions)):
            #            print enemy_minions[i]
            #        print ""
            #        player_minions = vision.all_minion_data(src,defines.player_minion_data_split,defines.c(defines.player_minions_box),minions_box_playable=defines.c(defines.reduced_player_minions_box),stage=stage)
            #        for i in range(0,len(player_minions)):
            #            print player_minions[i]
            #        for enemy_minion in enemy_minions:
            #            if enemy_minion['taunt']:
                            

        if enemy_minions != [] and enemy_minions != None:
            control_success=actions.move_and_leftclick(enemy_minions[e_m])
        elif enemy != [] and enemy != None:
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
        else:
            #something's wrong, try to attack any minion
            actions.pause_pensively(6)
            enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
            if enemy_minions != [] and enemy_minions != None:
                control_success=actions.move_and_leftclick(enemy_minions[0])
            else:
                actions.pause_pensively(6)
        control_success=actions.move_and_rightclick(c(defines.neutral_minion))
        actions.pause_pensively(1)
        src = vision.screen_cap()
        player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)

    #logging.info("---ATTACK WITH CHARACTER---")
    actions.pause_pensively(0.25)
    src = vision.screen_cap()
    player_attack  = vision.color_range_reduced_mids(src,c(defines.reduced_player_box),color='green')
    if player_attack != [] and player_attack != None and control_success:
        control_success=actions.move_and_leftclick(c(defines.neutral_minion))
        control_success=actions.move_and_leftclick(player_attack[0])
        actions.move_cursor([player_attack[0][0],player_attack[0][1]+10])
        actions.pause_pensively(0.35)
        src = vision.screen_cap()
        enemy=[]
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box1),color='red'))
        enemy.extend(vision.color_range_reduced_mids(src,c(defines.reduced_opponent_box2),color='red'))
        enemy_minions = vision.get_taunt_minions(src,c(defines.enemy_minions_box_taunts))
        if enemy_minions != []:
            e_m = randint(0,len(enemy_minions)-1) #attack a random taunt minion

        if enemy_minions != [] and enemy_minions != None:
            control_success=actions.move_and_leftclick(enemy_minions[e_m])
        elif enemy != [] and enemy != None:
            control_success=actions.move_and_leftclick(c(defines.opponent_hero))
        else:
            #something's wrong, try to attack any minion
            actions.pause_pensively(6)
            enemy_minions = vision.color_range_reduced_mids(src,c(defines.reduced_enemy_minions_box),color='red')
            if enemy_minions != [] and enemy_minions != None:
                control_success=actions.move_and_leftclick(enemy_minions[0])
        control_success=actions.move_and_leftclick(c(defines.neutral))
    
    #logging.info("------PLAY INFO CHECK-------")
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)
    if (player_cards==[] and player_ability ==[] and player_minions ==[]) or player_cards==None or player_ability == None or player_minions == None and control_success:
        #logging.info("---END TURN---")
        control_success=actions.move_and_leftclick(c(defines.neutral))
        player_turn_green_check = vision.color_range_reduced_mids(src,c(defines.turn_box),color='green')
        if player_turn_green_check !=[] and player_turn_green_check != None and control_success:
            control_success=actions.move_and_leftclick(c(defines.turn_button))
            control_success=actions.move_and_leftclick(c(defines.turn_button))
            control_success=actions.move_and_leftclick(c(defines.neutral))
        else:
            actions.pause_pensively(4)
            player_end()

def opponent():
    pass
def victory():
    #logging.info("Victory")
    control_success=actions.move_and_leftclick(c(defines.neutral))
def defeat():
    #logging.info("Defeat")
    control_success=actions.move_and_leftclick(c(defines.neutral))
def error():
    #logging.info("Error: Clicking OK in error message")
    control_success=actions.move_and_leftclick(c(defines.error))
def rank():
    control_success=actions.move_and_leftclick(c(defines.neutral))
    control_success=actions.move_and_leftclick(c(defines.main_screen_splash))
def player_end():
    global src#,character_descs,stage_descs
    global NEW_GAME,opponent_char,player_char

    #logging.info("------PLAY INFO CHECK-------")
    control_success=actions.move_and_leftclick(c(defines.neutral))
    src = vision.screen_cap()
    player_cards   = vision.get_playable_cards(src,c(defines.hand_box))
    player_ability = vision.color_range_reduced_mids(src,c(defines.reduced_ability_box),color='green')
    player_minions = vision.color_range_reduced_mids(src,c(defines.reduced_player_minions_box),color='green',min_threshold=45,max_threshold=200)

    if (player_cards==[] and player_ability ==[] and player_minions ==[]) or player_cards==None or player_ability == None or player_minions == None and control_success:
        #logging.info("---END TURN---")
        control_success=actions.move_and_leftclick(c(defines.turn_button))
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
                    if wait_count >= 10:
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
#The GUI
class App(Frame):
    def change_led_color(self,color,input):
        self.led.configure(background=color,text=input)

    def toggle_quest_reroll(self):
        if self.quest_button['background'] == "#00ff00":#color is green, so user is disabling
            self.quest_button.configure(background="#ff0000")
            defines.REROLL_QUESTS=False
        else:#color is red, so user is enabling
            self.quest_button.configure(background="#00ff00")
            defines.REROLL_QUESTS=True
        save_config()
            
    def toggle_mulligan(self):
        if self.mulligan_button['background'] == "#00ff00":#color is green, so user is disabling
            self.mulligan_button.configure(background="#ff0000")
            defines.MULLIGAN=False
        else:#color is red, so user is enabling
            self.mulligan_button.configure(background="#00ff00")
            defines.MULLIGAN=True
        save_config()
            
    def toggle_random_attack(self):
        if self.random_attack_button['background'] == "#00ff00":#color is green, so user is disabling
            self.random_attack_button.configure(background="#ff0000")
            defines.RANDOM_ATTACKS=False
        else:#color is red, so user is enabling
            self.random_attack_button.configure(background="#00ff00")
            defines.RANDOM_ATTACKS=True
        save_config()

    def toggle_move_mouse(self):
        if self.mouse_button['background'] == "#00ff00":#color is green, so user is disabling
            self.mouse_button.configure(background="#ff0000")
            defines.USE_MOUSE=False
        else:#color is red, so user is enabling
            self.mouse_button.configure(background="#00ff00")
            defines.USE_MOUSE=True
        save_config()

    def config_deckbutton(self,deck):
        deck-=1
        if self.deck_buttons[deck]['background'] == "#00ff00":#color is green, so user is disabling
            self.deck_buttons[deck].configure(background="#ff0000")
            defines.DECKS_TO_USE.remove(deck)
        else:#color is red, so user is enabling
            self.deck_buttons[deck].configure(background="#00ff00")
            defines.DECKS_TO_USE.append(deck)
        save_config()

    def toggle_deck_button1(self):
        self.config_deckbutton(1)
    def toggle_deck_button2(self):
        self.config_deckbutton(2)
    def toggle_deck_button3(self):
        self.config_deckbutton(3)
    def toggle_deck_button4(self):
        self.config_deckbutton(4)
    def toggle_deck_button5(self):
        self.config_deckbutton(5)
    def toggle_deck_button6(self):
        self.config_deckbutton(6)
    def toggle_deck_button7(self):
        self.config_deckbutton(7)
    def toggle_deck_button8(self):
        self.config_deckbutton(8)
    def toggle_deck_button9(self):
        self.config_deckbutton(9)
        
    def select_decks_to_use(self):
        deckwin = Toplevel(self)
        deckwin.resizable(0,0)
        custom_title = Label(deckwin,text="Select custom decks to use:",font=tkFont.nametofont("TkTextFont"))
        custom_title.grid(row=0,column=0,columnspan=3)
        self.deck_buttons=[]
        self.deck_buttons.append(Button(deckwin, text="1", command=self.toggle_deck_button1))
        self.deck_buttons.append(Button(deckwin, text="2", command=self.toggle_deck_button2))
        self.deck_buttons.append(Button(deckwin, text="3", command=self.toggle_deck_button3))
        self.deck_buttons.append(Button(deckwin, text="4", command=self.toggle_deck_button4))
        self.deck_buttons.append(Button(deckwin, text="5", command=self.toggle_deck_button5))
        self.deck_buttons.append(Button(deckwin, text="6", command=self.toggle_deck_button6))
        self.deck_buttons.append(Button(deckwin, text="7", command=self.toggle_deck_button7))
        self.deck_buttons.append(Button(deckwin, text="8", command=self.toggle_deck_button8))
        self.deck_buttons.append(Button(deckwin, text="9", command=self.toggle_deck_button9))
        for i in range(0,9):
            self.deck_buttons[i].grid(row=i/3+1,column=i%3)
            if i in defines.DECKS_TO_USE:
                self.deck_buttons[i].configure(background="#00ff00")
            else:
                self.deck_buttons[i].configure(background="#ff0000")

    def misc(self):
        deckwin = Toplevel(self)
        deckwin.resizable(0,0)
        custom_title = Label(deckwin,text="Toggle options:",font=tkFont.nametofont("TkTextFont"))
        custom_title.grid(row=0,column=0,columnspan=3)
        self.quest_button = Button(deckwin,    text="Reroll 40 gold quests  ",font=self.mediumfont, command=self.toggle_quest_reroll)
        self.quest_button.grid(row=1,column=1)
        if defines.REROLL_QUESTS:
            self.quest_button.configure(background="#00ff00")
        else:
            self.quest_button.configure(background="#ff0000")

        self.mulligan_button = Button(deckwin, text="Mulligan cards             ",font=self.mediumfont, command=self.toggle_mulligan)
        self.mulligan_button.grid(row=2,column=1)
        if defines.MULLIGAN:
            self.mulligan_button.configure(background="#00ff00")
        else:
            self.mulligan_button.configure(background="#ff0000")

        self.random_attack_button = Button(deckwin, state='disabled', text="Attack taunts randomly",font=self.mediumfont, command=self.toggle_random_attack)
        self.random_attack_button.grid(row=3,column=1)
        if defines.RANDOM_ATTACKS:
            self.random_attack_button.configure(background="#00ff00")
        else:
            self.random_attack_button.configure(background="#ff0000")

    def save_mouse_speed(self,speed):
        defines.MOUSE_SPEED=speed
        save_config()

    def save_start_hour(self,hour):
        defines.START_HOUR=int(hour)
        save_config()

    def save_stop_hour(self,hour):
        defines.STOP_HOUR=int(hour)
        save_config()

    def controls(self):
        deckwin = Toplevel(self)
        deckwin.resizable(0,0)
        custom_title = Label(deckwin,text="Control options:",font=tkFont.nametofont("TkTextFont"))
        custom_title.grid(row=0,column=0,columnspan=3)
        #self.mouse_button = Button(deckwin,    text="Move mouse         ",font=self.mediumfont, command=self.toggle_move_mouse)
        #self.mouse_button.grid(row=1,column=0)
        #if defines.USE_MOUSE:
        #    self.mouse_button.configure(background="#00ff00")
        #else:
        #    self.mouse_button.configure(background="#ff0000")

        mouse_speed_label = Label(deckwin,text="Mouse speed:",font=tkFont.nametofont("TkTextFont"))
        mouse_speed_label.grid(row=2,column=0)
        self.mouse_speed_scale = Scale(deckwin, from_=1, to=9,font=tkFont.nametofont("TkTextFont"), orient=HORIZONTAL,command=self.save_mouse_speed)
        self.mouse_speed_scale.grid(row=2,column=1)
        self.mouse_speed_scale.set(defines.MOUSE_SPEED)

        start_hour_label = Label(deckwin,text="Hour to start:",font=tkFont.nametofont("TkTextFont"))
        start_hour_label.grid(row=3,column=0)
        self.start_hour_scale = Scale(deckwin, from_=0, to=24,font=tkFont.nametofont("TkTextFont"), orient=HORIZONTAL,command=self.save_start_hour)
        self.start_hour_scale.grid(row=3,column=1)
        self.start_hour_scale.set(defines.START_HOUR)
        
        stop_hour_label = Label(deckwin,text="Hour to stop:",font=tkFont.nametofont("TkTextFont"))
        stop_hour_label.grid(row=4,column=0)
        self.stop_hour_scale = Scale(deckwin, from_=0, to=24,font=tkFont.nametofont("TkTextFont"), orient=HORIZONTAL,command=self.save_stop_hour)
        self.stop_hour_scale.grid(row=4,column=1)
        self.stop_hour_scale.set(defines.STOP_HOUR)

    def donate_window(self):
        donatewin = Toplevel(self)
        img = PhotoImage(data=qr.qrdata)
        self.qr_img = Label(donatewin, image = img)
        self.qr_img.image=img
        address='1KLTV69RzZSJEExic97q4btFuHRBgacEd3'
        self.donatetxt = Text(donatewin, borderwidth=3, relief="sunken", width=34, height=1)
        self.donatetxt.config(font=("consolas", 12), undo=True, wrap='word')
        self.donatetxt.insert(INSERT, address)
        self.donatetxt.config(state="disabled")
        self.donatetxt.pack()
        self.qr_img.pack()

    def help_window(self):
        def set_text_newline(s):
            self.txt.insert(INSERT, s+'\n')
        helpwin = Toplevel(self)
        # create a Frame for the Text and Scrollbar
        txt_frm = Frame(helpwin, width=600, height=600)
        txt_frm.pack(fill="both", expand=True)
        # ensure a consistent GUI size
        txt_frm.grid_propagate(False)
        # implement stretchability
        txt_frm.grid_rowconfigure(0, weight=1)
        txt_frm.grid_columnconfigure(0, weight=1)

        # create a Text widget
        self.txt = Text(txt_frm, borderwidth=3, relief="sunken")
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        set_text_newline("This is a Hearthstone color bot that takes screenshots of the game window and uses computer vision (sift and color masking) to find playable cards, use the character ability, and to attack with minions.")
        set_text_newline("")
        set_text_newline("How to use:")
        set_text_newline(" -Make custom decks that the bot can use and note their number in the list (1-9)")
        set_text_newline(" -Start Battle.net or start Hearthstone and start the bot   ")
        set_text_newline(" -Select the custom decks that the bot can use with Options->Custom Decks.  Green means use the deck, red means do not use the deck.")
        set_text_newline(" -Press start, the bot will attempt to start and use the game. It may take a couple of seconds.")
        set_text_newline(" -Press stop to stop the bot, it may take a couple of seconds.")
        set_text_newline("")
        set_text_newline("The bot takes control of the mouse. If it detects that the user is using the mouse, it will stop and pause for a couple of seconds.")
        set_text_newline("")
        set_text_newline("The bot can play simple minions or spells that don't have targeting abilities (such as 'give a minion +1/+1' or'deal 3 damage' or 'silence a minion'). Basically, if the card can be played by right-clicking, dragging, and right-clicking on the minion field, the bot will play it. Otherwise it might get stuck.")
        set_text_newline("")
        set_text_newline("If the game resolution is not 16:9 the bot will automatically convert it to 16:9.  The recommended resolutions are 1366x768, 1280x720, or 1920x1080. If the monitor resolution or game resolution is changed it is recommended to restart the bot. It is recommended to use the hearthstone client in windowed mode so it can be minimized easily.")
        set_text_newline("")
        set_text_newline("The bot will attempt to restart the game if it closes or disconnects.")
        set_text_newline("")
        set_text_newline("Gameplay:")
        set_text_newline("  -Reroll 40 gold quests: Check once per hour for new quests and reroll if they are for 40 gold")
        set_text_newline("  -Mulligan cards: If 3 cards, mulligan 4+ cost, if 4 cards mulligan 1 and 5+ cost.  This is to try to make better use of the coin on the first turn.")
        set_text_newline("  -Attack randomly: If this is red (off) the feature will attempt to read the values on all minions and attack enemy taunts using the minimum resources.")
        set_text_newline("")
        set_text_newline("Control options:")
        set_text_newline("  -Mouse speed: Increase or decrease the mouse speed")
        set_text_newline("  -Hour to start: Have the bot wait until a certain time to start, 1-24 military time (24=12am). Set the time, then press start, the bot will display what system time it is waiting until. 0 to disable")
        set_text_newline("  -Hour to stop: Have the bot pause when it reaches a certain time of day, 1-24 military time (24=12am). 0 to disable.  If Hour to start is set, it will start again at that time")
        set_text_newline("")
        set_text_newline("Options are saved to a config file.")
        set_text_newline("")
        set_text_newline("")
        self.txt.config(state="disabled")
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        scrollb = Scrollbar(txt_frm, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent 
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        self.mediumfont = tkFont.nametofont("TkFixedFont")
        self.mediumfont.configure(size=22)
        self.mediumfont.configure(family="Helvetica")

        optionsmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_command(label="Custom Decks", command=self.select_decks_to_use)
        optionsmenu.add_command(label="Gameplay", command=self.misc)
        optionsmenu.add_command(label="Controls", command=self.controls)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Options", menu=optionsmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.help_window)
        helpmenu.add_command(label="Donate Bitcoin!", command=self.donate_window)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self._job_id = None
        self._error  = ""
        self.parent.title(defines.titles[randint(0,len(defines.titles)-1)])
        self.parent.resizable(0,0)

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=42)
        self.led = Button(self,state='disabled')
        self.qmessage = Label(self,text="Edit the decks for the bot to use with Options->Custom_Decks before starting",font=tkFont.nametofont("TkTextFont"))
        self.start_button = Button(self, text="start", command=self.start_click)
        self.stop_button  = Button(self, text="stop", command=self.stop_click)

        self.start_button.grid(row=1,column=0,sticky='N')
        self.stop_button.grid(row=1,column=1,sticky='N')
        self.led.grid(row=1,column=2)
        self.qmessage.grid(row=0,column=0,columnspan=3)

        self.change_led_color("#ff0000"," off ")
        self.stop_button.config(state='disabled')
        
        self.queue       = Queue.Queue()
        self.logicthread = GameLogicThread(self.queue)

    def queue_message(self,msg):
        self.qmessage.configure(text=msg)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            if self._error != "":
                self.queue_message(self._error)
            else:
                if msg[0:5] == "Error":
                    self._error = msg
                    self.queue_message(msg)
                    self.stop_click()
                else:
                    self.queue_message(msg)
            self.after(100, self.process_queue)
        except Queue.Empty:
            self.after(100, self.process_queue)

    def stop_click(self):
        if self._job_id is not None:
            self.logicthread.stop()
            self.logicthread.join()
            self._job_id = None
            self.change_led_color("#ff0000"," off ")
            self.queue_message("")
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.queue       = Queue.Queue()
            self.logicthread = GameLogicThread(self.queue)
            self.queue.put("stopped")

    def start_click(self):
        if self._job_id is None:
            self._error = ""
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.change_led_color("#00ff00"," on ")
            self._job_id = True
            #reset thread
            self.queue       = Queue.Queue()
            self.logicthread = GameLogicThread(self.queue)
            self.logicthread.start()
            self.after(100, self.process_queue)

def save_config():
    f = open( 'config.txt', 'w' )
    f.write( 'DECKS_TO_USE          = ' + repr(defines.DECKS_TO_USE)       + '\n' )
    f.write( 'REROLL_QUESTS         = ' + str(int(defines.REROLL_QUESTS))  + '\n' )
    f.write( 'MULLIGAN              = ' + str(int(defines.MULLIGAN))       + '\n' )
    f.write( 'RANDOM_ATTACKS        = ' + str(int(defines.RANDOM_ATTACKS)) + '\n' )
    f.write( 'USE_MOUSE             = ' + str(int(defines.USE_MOUSE))       + '\n' )
    f.write( 'MOUSE_SPEED           = ' + str(int(defines.MOUSE_SPEED)) + '\n' )
    f.write( 'START_HOUR            = ' + str(int(defines.START_HOUR)) + '\n' )
    f.write( 'STOP_HOUR             = ' + str(int(defines.STOP_HOUR)) + '\n' )
    f.close()

def load_config():
    config_file = open( 'config.txt', 'r' )
    chars = config_file.readline()
    defines.DECKS_TO_USE = []
    for ch in chars:
        if ch.isdigit():
            defines.DECKS_TO_USE.append(int(ch))

    chars = config_file.readline()
    for ch in chars:
        if ch.isdigit():
            defines.REROLL_QUESTS   = int(ch)

    chars = config_file.readline()
    for ch in chars:
        if ch.isdigit():
            defines.MULLIGAN        = int(ch)

    chars = config_file.readline()
    for ch in chars:
        if ch.isdigit():
            defines.RANDOM_ATTACKS  = int(ch)

    chars = config_file.readline()
    for ch in chars:
        if ch.isdigit():
            defines.USE_MOUSE  = int(ch)

    chars = config_file.readline()
    for ch in chars:
        if ch.isdigit():
            defines.MOUSE_SPEED  = int(ch)
    
    chars = config_file.readline()
    total_ch=''
    for ch in chars:
        if ch.isdigit():
            total_ch+=ch
        else:
            total_ch+=''
    defines.START_HOUR  = int(total_ch)

    chars = config_file.readline()
    total_ch=''
    for ch in chars:
        if ch.isdigit():
            total_ch+=ch
        else:
            total_ch+=''
    defines.STOP_HOUR  = int(total_ch)

    config_file.close()

def main():
    global src
    global NEW_GAME
    #logging.basicConfig(filename='game.log',level=logging.DEBUG)

    #load config options
    load_config()

    #start the app window
    root = Tk()
    App(root).pack()
    root.mainloop()

if __name__ == '__main__':
    main()