from pair_convert import convert

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
origin          = [0,0]
screen_box      = (origin[0],origin[1],game_screen_res[0],game_screen_res[1])

ref_game_screen_res       = [1920,1080] #Scale mouse and info coords relative to this reference.
ref_origin                = [0,0]       #reference origin
neutral                   = [1284,894]  #nothing
neutral_minion            = [911,711]  #nothing while attacking with minions

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
    return convert(var,ref)

###############
#MOUSE COOORDS#
###############
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

confirm_hand_button       = [960,862]
turn_button               = [1552,496]
player_hero               = [962,838]
opponent_hero             = [952,204]
player_ability            = [1132,826]
player_deck               = [1622,650]
opponent_deck             = [1622,335]
opponent_hand             = [1010,73]
error                     = [957,576]
play_card_left            = [400,600]
play_card_right           = [1470,600]
play_card                 = [[1470,600],[400,600]]
bnet_games_button         = [173,46]
bnet_hearthstone_button   = [55,520]
bnet_play_button          = [282,966]
bnet_go_online_button     = [1820,60]
bnet_accept_pw_button     = [100,290]
bnet_launch_error_button  = [60,120]

############
# INFO BOX #
############
stage_box                   = (250,0,720,230)
hand_box                    = (540,1040,1330,1079)
turn_box                    = (1455,435,1640,540)
enemy_box                   = (910,133,1005,273)
player_box                  = (910,767,1005,902)
reduced_player_box          = (917,701,1012,745)
reduced_player_minions_box  = (421,504,1440,518)
reduced_ability_box         = (1066,744,1140,766)
reduced_enemy_minions_box   = (421,316,1440,332)
reduced_opponent_box1       = (877,128,913,142)
reduced_opponent_box2       = (1000,128,1037,137)

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
            (644,387,1216,510)]   #error

#############
# CONSTANTS #
#############
#0 1 2
#3 4 5 
#6 7 8
DECKS_TO_USE = [0,1,2,3,4,5,6,7,8]

class State:
    DESKTOP, HOME, PLAY, QUEUE, VERSUS, SELECT, WAIT, PLAYER, OPPONENT, VICTORY, DEFEAT, ERROR = range(0,12)

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
              'player_turn_green':7,
              'enemy_turn':8,
              'enemy_turn2':8,
              'enemy_turn3':8,
              'victory':9,
              'gold':9,
              'defeat':10,
              'error':11
             }