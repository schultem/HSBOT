from pairconvert import convert

#######################################
#  The game screen resolution to use  #
#  The upper left hand corner origin  #
#######################################
#valid resolutions (16:9):
#game_screen_res = [1920,1080]
#game_screen_res = [1280,720]
#game_screen_res = [1366,768]
#game_screen_res = [854,480]
game_screen_res = [1920,1080]
game_screen_res_list = [[1920,1080],
                        [1366,768],
                        [1280,720]
                       ]
origin          = [0,0]
screen_box      = (origin[0],origin[1],game_screen_res[0],game_screen_res[1])

ref_game_screen_res       = [1920,1080] #Scale mouse and info coords relative to this reference.
ref_game_screen_res_list = [[1920,1080],
                            [1920,1080],
                            [1920,1080]
                           ]
ref_origin                = [0,0]       #reference origin
neutral                   = [1284,894]  #nothing
neutral_minion            = [910,705]  #nothing while attacking with minions

#scale coords or boxs by the res to reference ratio, use with pair_convert and add origin offset
#def ref(x):
#    conv_ratio_ref  = ref_game_screen_res
#    conv_ratio      = game_screen_res
#
#    if isinstance(x,list):#2 list
#        return [int(x[0]*float(conv_ratio[0])/float(conv_ratio_ref[0]))+origin[0],int(x[1]*float(conv_ratio[1])/float(conv_ratio_ref[1]))+origin[1]]
#    if isinstance(x,tuple):#4 tuple
#        return (int(x[0]*float(conv_ratio[0])/float(conv_ratio_ref[0]))+origin[0],int(x[1]*float(conv_ratio[1])/float(conv_ratio_ref[1]))+origin[1],int(x[2]*float(conv_ratio[0])/float(conv_ratio_ref[0]))+origin[0],int(x[3]*float(conv_ratio[1])/float(conv_ratio_ref[1]))+origin[1])

#scale coords or boxs by the res to reference ratio, use with pair_convert and add origin offset
def ref(x):
    conv_ratio_ref  = ref_game_screen_res
    conv_ratio      = game_screen_res

    if isinstance(x,list):#2 list
        return [int(x[0]*float(conv_ratio[0])/float(conv_ratio_ref[0]))+origin[0],int(x[1]*float(conv_ratio[1])/float(conv_ratio_ref[1]))+origin[1]]
    if isinstance(x,tuple):#4 tuple
        return (int(x[0]*float(conv_ratio[0])/float(conv_ratio_ref[0]))+origin[0],int(x[1]*float(conv_ratio[1])/float(conv_ratio_ref[1]))+origin[1],int(x[2]*float(conv_ratio[0])/float(conv_ratio_ref[0]))+origin[0],int(x[3]*float(conv_ratio[1])/float(conv_ratio_ref[1]))+origin[1])

#A shorter function name to scale coords to the desired screen resolution
def c(var):
    new = var
    return convert(new,ref)

###############
#MOUSE COOORDS#
###############
main_menu_nuetral         = [1750,600]
main_menu_play_button     = [952,336]
main_menu_practice_button = [944,411]
custom_decks_arrow        = [890,995]
deck_locations            = {
                            0:[470,300],
                            1:[700,300],
                            2:[950,300],
                            3:[465,520],
                            4:[700,520],
                            5:[950,520],
                            6:[470,750],
                            7:[710,750],
                            8:[950,750],
                            }
play_button               = [1400,890]
play_back_button          = [1587,994]
quest_button              = [534,950]
reroll_quest_button_1     = [805,785]
reroll_quest_button_2     = [1050,785]
reroll_quest_button_3     = [1290,785]

starting_hand_costs_4     = [(459,350,515,400),(714,350,775,400),(965,350,1030,400),(1224,240,1284,400)]
starting_hand_costs_3     = [(490,350,555,400),(835,350,900,400),(1180,350,1240,400)]

confirm_hand_button       = [960,862]
turn_button               = [1552,496]
player_hero               = [962,838]
opponent_hero             = [952,204]
player_ability            = [1132,826]
player_deck               = [1622,650]
opponent_deck             = [1622,335]
opponent_hand             = [1010,73]
error_1                   = [957,576]
error_2                   = [957,600]
play_card                 = [[400,600],[960,600],[900,600],[1000,600],[1470,600]]
bnet_games_button         = [173,46]
bnet_hearthstone_button   = [55,425]
bnet_play_button          = [282,966]
bnet_go_online_button     = [1750,60]
bnet_accept_pw_button     = [100,290]
bnet_launch_error_button  = [60,120]
main_screen_splash        = [690,536]
ranked_button             = [1500,190]
casual_button             = [1300,190]
nuetral_targeting         = [680,770]

############
# INFO BOX #
############
quest_box_1                 = (680,885,750,920)
quest_box_2                 = (930,885,994,920)
quest_box_3                 = (1170,885,1236,920)
stage_box                   = (250,0,720,230)
hand_box                    = (540,1040,1330,1079)
turn_box                    = (1455,435,1640,540)
enemy_box                   = (910,133,1005,273)
player_box                  = (910,767,1005,902)
reduced_player_box          = (917,701,1012,745)
reduced_player_minions_box  = (421,504,1425,518)
player_minions_box          = (475,645,1425,680)
player_minion_data          = (440,625,1425,655)
player_minion_data_split    = [(485,625,525,655),(550,625,600,655),(630,625,670,655),(690,625,738,655),(760,625,810,655),(830,625,880,655),(900,625,950,655),(970,625,1020,655),(1040,625,1090,655),(1110,625,1155,655),(1188,625,1225,655),(1245,625,1295,655),(1325,625,1370,655),(1395,625,1435,655)]
reduced_ability_box         = (1066,744,1140,766)
enemy_minions_box_taunts    = (475,487,1445,500)
enemy_minions_box           = (470,470,1425,485)
enemy_minion_data           = (440,438,1425,466)
enemy_minion_data_split     = [(485,438,525,466),(550,438,600,466),(630,438,670,466),(690,438,738,466),(760,438,810,466),(830,438,880,466),(900,438,950,466),(970,438,1020,466),(1040,438,1090,466),(1110,438,1155,466),(1188,438,1225,466),(1245,438,1295,466),(1325,438,1370,466),(1395,438,1435,466)]
reduced_enemy_minions_box   = (421,316,1425,332)
reduced_opponent_box1       = (877,128,913,142)
reduced_opponent_box2       = (1000,128,1037,137)
nuetral_targeting_box       = (650,750,705,775)

state_box =[(0,1037,1920,1080),   #deskop
            (684,189,1214,676),   #home
            (517,12,915,75),      #play
            (715,150,1210,260),   #finding_opponent
            (840,400,1130,690),   #versus
            (730,135,1185,185),   #starting_hand
            (800,785,1130,820),   #opponent_still_choosing
            (1455,435,1640,540),  #player_turn
            (1455,435,1640,540),  #enemy_turn
            (725,580,1230,720),   #victory
            (725,580,1230,720),   #defeat
            (690,703,1283,845),   #gold
            (644,387,1216,510),   #error
            (800,330,1130,860)]   #rank

#############
# CONSTANTS #
#############
#0 1 2
#3 4 5 
#6 7 8
DECKS_TO_USE    = [0,1,2,3,4,5,6,7,8]
REROLL_QUESTS   = True
MULLIGAN        = True
RANDOM_ATTACKS  = True
PLAY_RANKED     = True
USE_MOUSE       = True
MOUSE_SPEED     = 5
START_HOUR      = 0
START_HOUR      = 0
TARGETING       = [0,0,0,0,0,0,0,0,0]
GAME_SCREEN_RES = 1

class Target:
    NONE, OPPONENT_HERO = range(0,2)

class State:
    DESKTOP, HOME, PLAY, QUEUE, VERSUS, SELECT, WAIT, PLAYER, OPPONENT, VICTORY, DEFEAT, ERROR, RANK, PLAYER_GREEN = range(0,14)

state_dict = {
              'desktop':0,
              'home':1,
              'play':2,
              'finding_opponent':3,
              'versus':4,
              'starting_hand':5,
              'opponent_still_choosing':6,
              'player_turn':7,
              'player_turn2':7,
              'player_turn3':7,
              'enemy_turn':8,
              'enemy_turn2':8,
              'enemy_turn3':8,
              'victory':9,
              'gold':9,
              'defeat':10,
              'error':11,
              'rank':12,
              'player_turn_green':13,
             }

titles = ["Untitled - Notepad","Administrator: C:\Windows\system32\cmd.exe","Untitled(100%) - Paint.NET v3.5.11","Mozilla Firefox","MySQL Command Line Client","GNU Image Manipulation Program"]