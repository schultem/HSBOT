import vision
import actions
import defines
import os

def main():
    #vision.screen_save()
    #src = vision.screen_load()
    src = vision.imread(os.getcwd() + '\\temp\\temp.png')

    #print defines.enemy_box
    #print defines.convert(defines.enemy_box,defines.ref)
    
    print "game state        : ",defines.state_dict[vision.get_state(src)]
    print "opponent char     : ",vision.get_image_info('character',src,defines.enemy_box)
    print "player char       : ",vision.get_image_info('character',src,defines.player_box)
    print "stage             : ",vision.get_image_info('stage',src,defines.stage_box)
    print "turn              : ",vision.get_image_info('turn',src,defines.turn_box)
    print "playable cards    : ",vision.get_playable_cards(src,defines.hand_box)
    print "player            : ",vision.color_range_reduced_mids(src,defines.reduced_player_box,color='green')
    print "player ability    : ",vision.color_range_reduced_mids(src,defines.reduced_ability_box,color='green')
    print "player minions    : ",vision.color_range_mids(src,defines.player_minions_box,color='green')
    print "enemy             : ",vision.color_range_reduced_mids(src,defines.reduced_opponent_box,color='red')
    print "enemy minions     : ",vision.color_range_reduced_mids(src,defines.reduced_enemy_minions_box,color='red')

if __name__ == '__main__':
    main()