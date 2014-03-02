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
neutral                   = [1920,0]    #nothing

#scale coords or boxs by the res to reference ratio, use with pair_convert
def ref(x):
    conv_ratio_ref  = ref_game_screen_res
    conv_ratio      = game_screen_res

    if isinstance(x,list):#2 list
        return [int(x[0]*float(conv_ratio[0])/float(conv_ratio_ref[0])),int(x[1]*float(conv_ratio[1])/float(conv_ratio_ref[1]))]
    if isinstance(x,tuple):#4 tuple
        return (int(x[0]*float(conv_ratio[0])/float(conv_ratio_ref[0])),int(x[1]*float(conv_ratio[1])/float(conv_ratio_ref[1])),int(x[2]*float(conv_ratio[0])/float(conv_ratio_ref[0])),int(x[3]*float(conv_ratio[1])/float(conv_ratio_ref[1])))

###############
#MOUSE COOORDS#
###############
main_menu_play_button     = [952,336]
main_menu_practice_button = [944,411]
custom_decks_arrow        = [890,995]
deck_locations            = {
                            1:[470,300],
                            2:[700,300],
                            3:[950,300],
                            4:[465,520],
                            5:[700,520],
                            6:[950,520],
                            7:[470,750],
                            8:[710,750],
                            9:[950,750],
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

#player_minions_even       = {1:[600,600],2:[740,600],3:[880,600],4:[1020,600],5:[1160,600],6:[1300,600]}
#player_minions_odd        = {1:[530,600],2:[670,600],3:[810,600],4:[950,600],5:[1090,600],6:[1230,600],7:[1510,600]}

#hand = {
#       1: {1:[920,980]},
#       2: {1:[860,1000],2:[980,1000]},
#       3: {1:[790,1000],2:[920,1000],3:[1050,1000]},
#       4: {1:[720,1000],2:[860,1000],3:[990,1000],4:[1120,1000]},
#       5: {1:[690,1000],2:[810,1000],3:[920,1000],4:[1030,1000],5:[1140,1000]},
#       6: {1:[686,1030],2:[780,1030],3:[860,1030],4:[950,1030], 5:[1050,1030],6:[1150,1030]},
#       7: {1:[660,1030],2:[750,1030],3:[830,1030],4:[910,1030], 5:[980,1030], 6:[1060,1030],7:[1150,1030]},
#       8: {1:[660,1045],2:[730,1045],3:[800,1045],4:[860,1045], 5:[930,1045], 6:[1000,1045],7:[1070,1045],8:[1160,1045]},
#       9: {1:[640,1045],2:[710,1045],3:[780,1045],4:[830,1045], 5:[890,1045], 6:[950,1045], 7:[1000,1045],8:[1070,1045],9:[1160,1045]},
#       10:{1:[630,1060],2:[700,1060],3:[760,1060],4:[800,1060], 5:[860,1060], 6:[910,1060], 7:[960,1060], 8:[1015,1060],9:[1070,1060],10:[1160,1060]},
#       }

############
# INFO BOX #
############
stage_box                   = (250,0,720,230)
hand_box                    = (540,1032,1330,1079)
turn_box                    = (1455,435,1640,540)
enemy_box                   = (910,133,1005,273)
player_box                  = (910,767,1005,902)
player_minions_box          = (415,495,1470,675)
reduced_player_box          = (917,701,1012,745)
reduced_ability_box         = (1066,744,1140,766)
reduced_enemy_minions_box   = (415,316,1470,332)
reduced_opponent_box        = (900,91,1023,114)

state_box =[(0,1037,1920,1080),   #deskop
            (684,189,1214,676),   #home
            (517,12,915,75),      #play
            (715,150,1210,260),   #finding_opponent
            (840,400,1130,690),   #versus
            (730,135,1185,185),   #starting_hand
            (800,785,1130,820),   #opponent_still_choosing
            (1455,435,1640,540),  #player_turn
            (1455,435,1640,540),  #enemy_turn
            (790,1000,1130,1039)] #end

#############
# CONSTANTS #
#############
class State:
    Desktop, Home, Play, Queue, Versus, Select, Wait, Player, Opponent, End = range(0,10)

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
              'player_turn_green':7,
              'enemy_turn':8,
              'enemy_turn2':8,
              'end':9
             }