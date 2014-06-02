import defines

def save_config():
    f = open( 'config.txt', 'w' )
    f.write( 'DECKS_TO_USE          = ' + repr(defines.DECKS_TO_USE)       + '\n' )
    f.write( 'TARGETING             = ' + repr(defines.TARGETING)          + '\n' )
    f.write( 'REROLL_QUESTS         = ' + str(int(defines.REROLL_QUESTS))  + '\n' )
    f.write( 'MULLIGAN              = ' + str(int(defines.MULLIGAN))       + '\n' )
    f.write( 'RANDOM_ATTACKS        = ' + str(int(defines.RANDOM_ATTACKS)) + '\n' )
    f.write( 'USE_MOUSE             = ' + str(int(defines.USE_MOUSE))      + '\n' )
    f.write( 'PLAY_PRACTICE         = ' + str(int(defines.PLAY_PRACTICE))  + '\n' )
    f.write( 'PLAY_RANKED           = ' + str(int(defines.PLAY_RANKED))    + '\n' )
    f.write( 'MOUSE_SPEED           = ' + str(int(defines.MOUSE_SPEED))    + '\n' )
    f.write( 'START_HOUR            = ' + str(int(defines.START_HOUR))     + '\n' )
    f.write( 'STOP_HOUR             = ' + str(int(defines.STOP_HOUR))      + '\n' )
    f.write( 'GAME_SCREEN_RES       = ' + str(int(defines.GAME_SCREEN_RES))+ '\n' )
    f.close()

def load_config():
    config_file = open( 'config.txt', 'r' )
    chars = config_file.readline()
    defines.DECKS_TO_USE = []
    for ch in chars:
        if ch.isdigit():
            defines.DECKS_TO_USE.append(int(ch))

    chars = config_file.readline()
    defines.TARGETING = []
    for ch in chars:
        if ch.isdigit():
            defines.TARGETING.append(int(ch))

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
            defines.PLAY_PRACTICE  = int(ch)

    chars = config_file.readline()
    for ch in chars:
        if ch.isdigit():
            defines.PLAY_RANKED  = int(ch)

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

    chars = config_file.readline()
    total_ch=''
    for ch in chars:
        if ch.isdigit():
            total_ch+=ch
        else:
            total_ch+=''
    defines.GAME_SCREEN_RES  = int(total_ch)

    config_file.close()
