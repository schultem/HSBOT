import defines
import logging
from random import randint
from Tkinter import *
import tkFont
import Queue
import qr
from config import load_config,save_config
from playthread import *
#logging.basicConfig(filename='game.txt',level=logging.DEBUG)

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
        
    def toggle_play_ranked(self):
        if self.play_ranked_button['background'] == "#00ff00":#color is green, so user is disabling
            self.play_ranked_button.configure(background="#ff0000")
            defines.PLAY_RANKED=False
        else:#color is red, so user is enabling
            self.play_ranked_button.configure(background="#00ff00")
            defines.PLAY_RANKED=True
        save_config()
        
    def toggle_play_practice(self):
        if self.play_practice_button['background'] == "#00ff00":#color is green, so user is disabling
            self.play_practice_button.configure(background="#ff0000")
            defines.PLAY_PRACTICE=False
        else:#color is red, so user is enabling
            self.play_practice_button.configure(background="#00ff00")
            defines.PLAY_PRACTICE=True
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

    def config_deckbutton(self):
        deck=self.current_deckopt_num
        if self.deck_buttons[deck]['background'] == "#00ff00":#color is green, so user is disabling
            self.deck_buttons[deck].configure(background="#ff0000")
            self.deckopt_button.configure(background="#ff0000",text="Deck %i Disabled"%(deck+1))
            defines.DECKS_TO_USE.remove(deck)
        else:#color is red, so user is enabling
            self.deck_buttons[deck].configure(background="#00ff00")
            self.deckopt_button.configure(background="#00ff00",text="Deck %i Enabled "%(deck+1))
            defines.DECKS_TO_USE.append(deck)
        save_config()

    def config_preferences(self):
        defines.TARGETING[self.current_deckopt_num]=self.target.get()
        save_config()
        
    def config_resolution(self):
        defines.GAME_SCREEN_RES=self.resvar.get()
        save_config()

    def close_deck_opt(self):
        self.deckopt.destroy()
        self.deckopt=False

    def deck_options(self,decknum):
        if not self.deckopt:
            self.deckopt = Toplevel(self)
            self.deckopt.resizable(0,0)
            self.deckopt.protocol('WM_DELETE_WINDOW', self.close_deck_opt)
            self.current_deckopt_num = decknum-1

            custom_title = Label(self.deckopt,text="Deck %i options:"%decknum,font=tkFont.nametofont("TkTextFont"))
            custom_title.grid(row=0,column=0)
            
            self.deckopt_button = Button(self.deckopt, text="Deck %i enabled"%decknum,font=self.mediumfont, command=self.config_deckbutton)
            self.deckopt_button.grid(row=1,column=0)
            if self.current_deckopt_num in defines.DECKS_TO_USE:
                self.deckopt_button.configure(background="#00ff00",text="Deck %i Enabled "%decknum)
            else:
                self.deckopt_button.configure(background="#ff0000",text="Deck %i Disabled"%decknum)

            self.target = IntVar()
            self.target.set(defines.TARGETING[self.current_deckopt_num])
            Label(self.deckopt,text="Targeting preference:",         font=tkFont.nametofont("TkTextFont")).grid(row=2,column=0,sticky=W)
            Radiobutton(self.deckopt, text="No targeting",           font=tkFont.nametofont("TkTextFont"), variable=self.target, value=0, command=self.config_preferences).grid(row=3,column=0,sticky=W)
            Radiobutton(self.deckopt, text="Opponent hero",          font=tkFont.nametofont("TkTextFont"), variable=self.target, value=1, command=self.config_preferences).grid(row=4,column=0,sticky=W)
            #Radiobutton(self.deckopt, text="Enemy taunt minion",     font=tkFont.nametofont("TkTextFont"), variable=self.target, value=2, command=self.config_preferences).grid(row=5,column=0,sticky=W)
            #Radiobutton(self.deckopt, text="Random friendly minion", font=tkFont.nametofont("TkTextFont"), variable=self.target, value=3, command=self.config_preferences).grid(row=6,column=0,sticky=W)

        else:
            self.close_deck_opt()
            self.deck_options(decknum)

    def toggle_deck_button1(self):
        self.deck_options(1)
    def toggle_deck_button2(self):
        self.deck_options(2)
    def toggle_deck_button3(self):
        self.deck_options(3)
    def toggle_deck_button4(self):
        self.deck_options(4)
    def toggle_deck_button5(self):
        self.deck_options(5)
    def toggle_deck_button6(self):
        self.deck_options(6)
    def toggle_deck_button7(self):
        self.deck_options(7)
    def toggle_deck_button8(self):
        self.deck_options(8)
    def toggle_deck_button9(self):
        self.deck_options(9)

    def close_decks_to_use(self):
        self.deckwin.destroy()
        self.deckwin=False

    def select_decks_to_use(self):
        if not self.deckwin:
            self.deckwin = Toplevel(self)
            self.deckwin.resizable(0,0)
            self.deckwin.protocol('WM_DELETE_WINDOW', self.close_decks_to_use)
            custom_title = Label(self.deckwin,text="Select custom decks to use:",font=tkFont.nametofont("TkTextFont"))
            custom_title.grid(row=0,column=0,columnspan=3)
            self.deck_buttons=[]
            self.deck_buttons.append(Button(self.deckwin, text="1", command=self.toggle_deck_button1))
            self.deck_buttons.append(Button(self.deckwin, text="2", command=self.toggle_deck_button2))
            self.deck_buttons.append(Button(self.deckwin, text="3", command=self.toggle_deck_button3))
            self.deck_buttons.append(Button(self.deckwin, text="4", command=self.toggle_deck_button4))
            self.deck_buttons.append(Button(self.deckwin, text="5", command=self.toggle_deck_button5))
            self.deck_buttons.append(Button(self.deckwin, text="6", command=self.toggle_deck_button6))
            self.deck_buttons.append(Button(self.deckwin, text="7", command=self.toggle_deck_button7))
            self.deck_buttons.append(Button(self.deckwin, text="8", command=self.toggle_deck_button8))
            self.deck_buttons.append(Button(self.deckwin, text="9", command=self.toggle_deck_button9))
            for i in range(0,9):
                self.deck_buttons[i].grid(row=i/3+1,column=i%3)
                if i in defines.DECKS_TO_USE:
                    self.deck_buttons[i].configure(background="#00ff00")
                else:
                    self.deck_buttons[i].configure(background="#ff0000")
        else:
            self.close_decks_to_use()
            self.select_decks_to_use()

    def misc(self):
        self.miscwin = Toplevel(self)
        self.miscwin.resizable(0,0)
        custom_title = Label(self.miscwin,text="Toggle options:",font=tkFont.nametofont("TkTextFont"))
        custom_title.grid(row=0,column=0,columnspan=3)
        self.quest_button = Button(self.miscwin,    text="Reroll 40 gold quests  ",font=self.mediumfont, command=self.toggle_quest_reroll)
        self.quest_button.grid(row=1,column=1)
        if defines.REROLL_QUESTS:
            self.quest_button.configure(background="#00ff00")
        else:
            self.quest_button.configure(background="#ff0000")

        self.mulligan_button = Button(self.miscwin, text="Mulligan cards             ",font=self.mediumfont, command=self.toggle_mulligan)
        self.mulligan_button.grid(row=2,column=1)
        if defines.MULLIGAN:
            self.mulligan_button.configure(background="#00ff00")
        else:
            self.mulligan_button.configure(background="#ff0000")

        self.play_ranked_button = Button(self.miscwin, text="Play ranked                  ",font=self.mediumfont, command=self.toggle_play_ranked)
        self.play_ranked_button.grid(row=3,column=1)
        if defines.PLAY_RANKED:
            self.play_ranked_button.configure(background="#00ff00")
        else:
            self.play_ranked_button.configure(background="#ff0000")

        self.play_practice_button = Button(self.miscwin, text="Play practice                ",font=self.mediumfont, command=self.toggle_play_practice)
        self.play_practice_button.grid(row=4,column=1)
        if defines.PLAY_PRACTICE:
            self.play_practice_button.configure(background="#00ff00")
        else:
            self.play_practice_button.configure(background="#ff0000")

        self.random_attack_button = Button(self.miscwin, text="Attack taunts randomly",font=self.mediumfont, command=self.toggle_random_attack)
        self.random_attack_button.grid(row=5,column=1)
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
        self.controlwin = Toplevel(self)
        self.controlwin.resizable(0,0)
        custom_title = Label(self.controlwin,text="Control options:",font=tkFont.nametofont("TkTextFont"))
        custom_title.grid(row=0,column=0,columnspan=3)
        #self.mouse_button = Button(self.controlwin,    text="Move mouse         ",font=self.mediumfont, command=self.toggle_move_mouse)
        #self.mouse_button.grid(row=1,column=0)
        #if defines.USE_MOUSE:
        #    self.mouse_button.configure(background="#00ff00")
        #else:
        #    self.mouse_button.configure(background="#ff0000")

        mouse_speed_label = Label(self.controlwin,text="Mouse speed:",font=tkFont.nametofont("TkTextFont"))
        mouse_speed_label.grid(row=2,column=0)
        self.mouse_speed_scale = Scale(self.controlwin, from_=1, to=9,font=tkFont.nametofont("TkTextFont"), orient=HORIZONTAL,command=self.save_mouse_speed)
        self.mouse_speed_scale.grid(row=2,column=1)
        self.mouse_speed_scale.set(defines.MOUSE_SPEED)

        start_hour_label = Label(self.controlwin,text="Hour to start:",font=tkFont.nametofont("TkTextFont"))
        start_hour_label.grid(row=3,column=0)
        self.start_hour_scale = Scale(self.controlwin, from_=0, to=24,font=tkFont.nametofont("TkTextFont"), orient=HORIZONTAL,command=self.save_start_hour)
        self.start_hour_scale.grid(row=3,column=1)
        self.start_hour_scale.set(defines.START_HOUR)
        
        stop_hour_label = Label(self.controlwin,text="Hour to stop:",font=tkFont.nametofont("TkTextFont"))
        stop_hour_label.grid(row=4,column=0)
        self.stop_hour_scale = Scale(self.controlwin, from_=0, to=24,font=tkFont.nametofont("TkTextFont"), orient=HORIZONTAL,command=self.save_stop_hour)
        self.stop_hour_scale.grid(row=4,column=1)
        self.stop_hour_scale.set(defines.STOP_HOUR)
        
    def resolutions(self):
        self.resolutionwin = Toplevel(self)
        self.resolutionwin.resizable(0,0)
        custom_title = Label(self.resolutionwin,text="Resolutions:",font=tkFont.nametofont("TkTextFont"))
        custom_title.grid(row=0,column=0)

        #self.resvar = IntVar()
        #self.resvar.set(defines.GAME_SCREEN_RES)
        #print self.resvar.get()
        ##for i in xrange(len(defines.game_screen_res_list)):
        #i=0
        #Radiobutton(self.resvar, text='Test',font=tkFont.nametofont("TkTextFont"), variable=self.resvar, value=0, command=self.config_resolution).grid(row=i+1,column=0,sticky=W)
        
        self.resvar = IntVar()
        self.resvar.set(defines.GAME_SCREEN_RES)
        for i in xrange(len(defines.game_screen_res_list)):
            Radiobutton(self.resolutionwin, text=str(defines.game_screen_res_list[i]),font=tkFont.nametofont("TkTextFont"), variable=self.resvar, value=i, command=self.config_resolution).grid(row=i+1,column=0,sticky=W)

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
        set_text_newline("Build 6/1/2014 Version 2.0")
        set_text_newline("")
        set_text_newline("This is a Hearthstone color bot that takes screenshots of the game window and uses computer vision (sift and color masking) to find playable cards, use the character ability, and to attack with minions.")
        set_text_newline("")
        set_text_newline("How to use:")
        set_text_newline(" -Make custom decks that the bot can use and note their number in the list (1-9)")
        set_text_newline(" -Start Battle.net or start Hearthstone and start the bot   ")
        set_text_newline(" -Pick desired resolution from Controls->Resolutions")
        set_text_newline(" -Select the custom decks that the bot can use with Options->Custom Decks.  Green means use the deck, red means do not use the deck.")
        set_text_newline(" -Press start, the bot will attempt to start and use the game. It may take a couple of seconds.")
        set_text_newline(" -Press stop to stop the bot, it may take a couple of seconds.")
        set_text_newline("")
        set_text_newline("The bot takes control of the mouse. If it detects that the user is using the mouse, it will stop and pause momentarily.")
        set_text_newline("")
        set_text_newline("The bot can play simple minions or spells. Opponent hero targeting spells and minions can be enabled from the deck selection menu(all targeting cards will target the enemy hero).")
        set_text_newline("")
        set_text_newline("The bot will attempt to restart the game if it closes or disconnects.")
        set_text_newline("")
        set_text_newline("Gameplay:")
        set_text_newline("  -Reroll 40 gold quests: Check once per hour for new quests and reroll if they are for 40 gold")
        set_text_newline("  -Mulligan cards: If 3 cards, mulligan 4+ cost, if 4 cards mulligan 1 and 5+ cost.  This is to try to make better use of the coin on the first turn.")
        set_text_newline("  -Play ranked: Will select to play casual or ranked in Play mode.  This does nothing in practice mode")
        set_text_newline("  -Play practice: Play in practice mode (green) or Play mode (red)")
        set_text_newline("  -Attack randomly: If this is red (off) the feature will attempt to read the values on all minions and attack enemy taunts using the minimum resources.")
        set_text_newline("     NOTE: Currently for 4:3 resolutions this does not work and is disabled for those resolutions.")
        set_text_newline("")
        set_text_newline("Control options:")
        set_text_newline("  -Mouse speed: Increase or decrease the mouse speed")
        set_text_newline("  -Hour to start: Have the bot wait until a certain time to start, 1-24 military time (24=12am). Set the time, then press start, the bot will display what system time it is waiting until. 0 to disable")
        set_text_newline("  -Hour to stop: Have the bot pause when it reaches a certain time of day, 1-24 military time (24=12am). 0 to disable.  If Hour to start is set, it will start again at that time")
        set_text_newline("")
        set_text_newline("Resolutions:")
        set_text_newline("  -Pick the desired resolution to use the game window in.")
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
        optionsmenu.add_command(label="Resolution", command=self.resolutions)
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
        
        self.deckopt=False
        self.deckwin=False
        
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

def main():
    global src
    global NEW_GAME

    #load config options
    load_config()

    #start the app window
    root = Tk()
    App(root).pack()
    root.mainloop()

if __name__ == '__main__':
    main()