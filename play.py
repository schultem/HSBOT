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

#Store screen captures
src = None

#pre-calulate sift descriptors
state_descs     = vision.get_descs(os.getcwd()+ '\\images\\state\\')
character_descs = vision.get_descs(os.getcwd()+ '\\images\\character\\')
stage_descs     = vision.get_descs(os.getcwd()+ '\\images\\stage\\')
opponent_char=None
player_char=None

#get monitor resolution
monitor_x=actions.win32api.GetSystemMetrics(0)
monitor_y=actions.win32api.GetSystemMetrics(1)
defines.screen_box = (0,0,monitor_x,monitor_y)

#Shorter binding for the coord resolution convert function
def c(var):
    new = var
    return defines.convert(var,defines.ref)

#Update monitor resolution and game screen location and resolution
def update_resolutions():
    client_box              = actions.get_client_box("Hearthstone")
    defines.origin          = [client_box[0],client_box[1]]
    defines.game_screen_res = [client_box[2]-client_box[0],client_box[3]-client_box[1]]

#Flags
NEW_GAME = False

def desktop():
    pass
def home():
    actions.move_and_leftclick(c(defines.main_menu_play_button))
def play():
    if len(defines.DECKS_TO_USE):
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
    global src,character_descs,stage_descs
    global NEW_GAME,opponent_char,player_char
    actions.pause_pensively(1)

    if NEW_GAME:
        #logging.info("-------------NEW GAME INFO--------------")
        #opponent_char=vision.get_image_info_sift(src,character_descs,c(defines.enemy_box))
        #logging.info("OPPONENT: %s"%(opponent_char))
        #player_char=vision.get_image_info_sift(src,character_descs,c(defines.player_box))
        #logging.info("PLAYER:   %s"%(player_char))
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
    actions.pause_pensively(2)
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
    #logging.info("Victory")
    actions.move_and_leftclick(c(defines.neutral))
def defeat():
    #logging.info("Defeat")
    actions.move_and_leftclick(c(defines.neutral))
def error():
    #logging.info("Error: Clicking OK in error message")
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
                      4:'waiting',
                      5:'exchange cards',
                      6:'waiting',
                      7:'bot turn',
                      8:'opponent turn',
                      9:'waiting',
                      10:'waiting',
                      11:'error'
                     }
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.new_state=0
        self.old_state=0
        self.queue.put("Starting bot")
        while(not self.stopped()):
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
                            actions.move_and_leftclick(c(defines.error))
                            actions.move_and_leftclick(c(defines.neutral))
                
                    except:
                        self.queue.put("Error: Invalid state, starting the bot again may help")
                        self.stop()
            else:
                self.queue.put("Error: Battle.net may not be running, please start Battle.net")
                self.stop()

            self.queue.put(self.state_desc[self.new_state])
            if self.new_state != defines.State.DESKTOP and not self.stopped():
                states[self.new_state]()
            elif self.new_state == defines.State.DESKTOP and not self.stopped():
                #on the desktop for some reason, try to start the game or reshow the window if it's already running
                actions.pause_pensively(5)
                if not self.stopped():
                    actions.restart_game()
                    update_resolutions()
                    actions.move_and_leftclick(c(defines.neutral))
            self.old_state=self.new_state

#The GUI
class App(Frame):
    def change_led_color(self,color,input):
        self.led.configure(background=color,text=input)

    def config_deckbutton(self,deck):
        deck-=1
        if self.deck_buttons[deck]['background'] == "#00ff00":#color is green, so user is disabling
            self.deck_buttons[deck].configure(background="#ff0000")
            defines.DECKS_TO_USE.remove(deck)
        else:#color is red, so user is enabling
            self.deck_buttons[deck].configure(background="#00ff00")
            defines.DECKS_TO_USE.append(deck)

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

    def donate_window(self):
        donatewin = Toplevel(self)
        donatewin.resizable(0,0)
        custom_title = Label(donatewin,text="Bitcoin",font=tkFont.nametofont("TkTextFont"))

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
        set_text_newline("The bot can play simple minions or spells that don't have targeting abilities (such as 'give a minion +1/+1' or'deal 3 damage' or 'silence a minion'). Basically, if the card can be played by right-clicking, dragging, and right-clicking on the minion field, the bot will play it. Otherwise it will might get stuck.")
        set_text_newline("")
        set_text_newline("If the game resolution is not 16:9 the bot will automatically convert it to 16:9.  The recommended resolutions are 1366x768, 1280x720, or 1920x1080. If the monitor resolution or game resolution is changed it is recommended to restart the bot. It is recommended to use the hearthstone client in windowed mode so it can be minimized easily.")
        set_text_newline("")
        set_text_newline("The bot will attempt to restart the game if it closes or disconnects.")
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
        optionsmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_command(label="Custom Decks", command=self.select_decks_to_use)
        optionsmenu.add_separator()
        optionsmenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Options", menu=optionsmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.help_window)
        #helpmenu.add_command(label="Donate", command=self.donate_window)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self._job_id = None
        self._error  = ""
        self.parent.title("BBOT")
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

def main():
    global src
    global NEW_GAME
    #logging.basicConfig(filename='game.log',level=logging.DEBUG)

    #start the app window
    root = Tk()
    App(root).pack()
    root.mainloop()

if __name__ == '__main__':
    main()