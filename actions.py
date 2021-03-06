import win32api, win32con, win32gui, win32ui, win32process
import time
import defines
import vision
import logging
import random
#logging.basicConfig(filename='game.txt',level=logging.DEBUG)

def leftClick(click=True,coords=False,pycmdwnd=False):
    logging.info("[ENTER] leftClick")
    if click:
        try:
            if defines.USE_MOUSE:
                pause_pensively(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            else:
                pause_pensively(0.1)
                if pycmdwnd: 
                    pycwnd=pycmdwnd
                else:
                    whndl =  get_whndl("Hearthstone")
                    pycwnd = make_pycwnd(whndl)
                pycwnd_click(pycwnd,coords)
        except:
            print 'click error'
        pause_pensively(0.1)

def rightClick(click=True):
    logging.info("[ENTER] rightClick")
    if click:
        pause_pensively(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        pause_pensively(0.1)

def leftDown(click=True):
    logging.info("[ENTER] leftDown")
    if click:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)

def leftUp(click=True):
    logging.info("[ENTER] leftUp")
    if click:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(.1)

def setCursorPos(coord):
    #logging.info("[ENTER] setCursorPos")
    win32api.SetCursorPos((coord[0],coord[1]))

def getCursorPos():
    x,y = win32api.GetCursorPos()
    return [x,y]

def interpCursorPos(coord):
    logging.info("[ENTER] interpCursorPos")
    coord[0]+=random.randrange(-3, 3)#randomize the coordinate a bit
    coord[1]+=random.randrange(-3, 3)
    coord_curr = getCursorPos()
    newpos  = coord_curr
    while(coord_curr[0]!=coord[0] or coord_curr[1]!=coord[1]):        
        coord_curr = getCursorPos()
        #if the user is moving the mouse, break
        if coord_curr != newpos:
            return False
        if (coord_curr[0]<coord[0]):
            xd=1
        elif (coord_curr[0]>coord[0]):
            xd=-1
        else:
            xd=0
        if (coord_curr[1]<coord[1]):
            yd=1
        elif (coord_curr[1]>coord[1]):
            yd=-1
        else:
            yd=0
        newpos=[coord_curr[0]+xd,coord_curr[1]+yd]
        setCursorPos(newpos)
        for i in range(0,20000*(10-int(defines.MOUSE_SPEED))/5):    #pause
            i=i+1
    pause_pensively(0.1)
    return True

def pause_pensively(s):
    logging.info("[ENTER] pause_pensively")
    ratio = random.randrange(-25, 25)/100. #25 percent random difference
    time.sleep(s+s*ratio)


def leftclick_move_and_leftclick(click_coord, click_coord_2):
    logging.info("[ENTER] leftclick_move_and_leftclick")
    success = True
    if defines.USE_MOUSE and success:
        success = interpCursorPos(click_coord)
    pause_pensively(0.1)
    leftClick(success,click_coord)
    if defines.USE_MOUSE and success:
        success = interpCursorPos(click_coord_2)
    leftClick(success,click_coord_2)

def move_and_leftclick(click_coord,pycmdwnd=False):
    logging.info("[ENTER] move_and_leftclick")
    success = True
    if defines.USE_MOUSE and success:
        success = interpCursorPos(click_coord)
    
    leftClick(success,click_coord,pycmdwnd)
    return success

def move_and_rightclick(click_coord):
    logging.info("[ENTER] move_and_rightclick")
    success = True
    success = interpCursorPos(click_coord)
    rightClick(success)
    return success

def move_cursor(move_coord):
    logging.info("[ENTER] move_cursor")
    if defines.USE_MOUSE:
        success = interpCursorPos(move_coord)

def get_whndl(window_name):
    logging.info("[ENTER] get_whndl")
    whndl = win32gui.FindWindowEx(0, 0, None, window_name)
    return whndl

def make_pycwnd(hwnd):       
    logging.info("[ENTER] make_pycwnd")
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd

def pycwnd_click(pycwnd,coord):
    logging.info("[ENTER] pycwnd_click")
    lParam = coord[1] << 16 | coord[0]
    pycwnd.PostMessage(win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam);
    pause_pensively(0.1)
    pycwnd.PostMessage(win32con.WM_LBUTTONUP, 0, lParam);
    pause_pensively(0.1)

def foreground_whndl(whwnd):
    logging.info("[ENTER] foreground_whndl")
    win32gui.SetForegroundWindow(whwnd)

def pycwnd_string(pycwnd, msg):
    logging.info("[ENTER] pycwnd_string")
    for c in msg:
        if c == "\n":
            pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            pause_pensively(0.5)
            pycwnd.SendMessage(win32con.WM_CHAR, ord(c), 0)

def whnds_to_text(hwnds):
    logging.info("[ENTER] whnds_to_text")
    for hwnd in range(0,len(hwnds)):
        hwnds[hwnd]=win32gui.GetWindowText(hwnds[hwnd])
    return hwnds

def print_all_whnds():
    logging.info("[ENTER] print_all_whnds")
    hwnds=[]
    def enumHandler(hwnd, lParam):
        hwnds.append(hwnd)

    win32gui.EnumWindows(enumHandler, None)
    text_hwnds = whnds_to_text(hwnds)
    print text_hwnds

#Return True if game is not minimized and is running.  Otherwise False
def check_bnet(title):
    logging.info("[ENTER] check_bnet")
    whndl =  get_whndl(title)
    if whndl != None and whndl != 0:
        return True
    return False

#Return True if game is not minimized and is running.  Otherwise False
def check_game(title):
    logging.info("[ENTER] check_game")
    whndl =  get_whndl(title)
    if whndl != None and whndl != 0:
        #check if game is not minimized
        f_whndl= win32gui.GetForegroundWindow()
        if f_whndl == whndl:
            return True
    return False
    
#Return True if game is running.  Otherwise False
def game_running(title):
    logging.info("[ENTER] check_game")
    whndl =  get_whndl(title)
    if whndl != None and whndl != 0:
        return True
    return False

def get_client_box(title):
    logging.info("[ENTER] get_client_box")
    whndl =  get_whndl(title)
    if whndl != None and whndl != 0:
        window_box = win32gui.GetWindowRect(whndl)
        client_box = win32gui.GetClientRect(whndl)
    else:
        #default
        window_box = defines.screen_box
        client_box = defines.screen_box

    border_size=(window_box[2]-window_box[0]-client_box[2])/2
    label_size=(window_box[3]-window_box[1]-client_box[3])-border_size
    return (window_box[0]+border_size,window_box[1]+label_size,window_box[2]-border_size,window_box[3]-border_size)

#change ratio of input list to closest value of output ratio
#use here is to get game close to 16:9 resolution so the button locations work
def closest_ratio(r_input,r_output):
    logging.info("[ENTER] closest_ratio")
    if r_input != None and r_input[1] !=0:
        if float(r_input[0])/float(r_input[1]) > r_output:
            change_var = r_input[0]
            while float(change_var)/float(r_input[1]) > r_output:
                change_var-=1
            return [change_var,r_input[1]]
        else:
            change_var = r_input[0]
            while float(change_var)/float(r_input[1]) < r_output:
                change_var+=1
            return [change_var,r_input[1]]
    return r_input

#Move game window to 0,0 and update it to represent the the clients desired resolution
def reset_game_window():
    logging.info("[ENTER] reset_game_window")
    title="Hearthstone"
    game_whndl =  get_whndl(title)
    if game_whndl != None and game_whndl != 0:
        win32gui.ShowWindow(game_whndl, win32con.SW_RESTORE)
        foreground_whndl(game_whndl)
        client_box              = get_client_box(title)
        #defines.game_screen_res = [client_box[2]-client_box[0],client_box[3]-client_box[1]]
        #defines.game_screen_res = closest_ratio(defines.game_screen_res,16/9.)
        win32gui.MoveWindow(game_whndl,0,0,defines.game_screen_res_list[defines.GAME_SCREEN_RES][0],defines.game_screen_res_list[defines.GAME_SCREEN_RES][1],True)

        defines.origin = [0,0]#explicitly updated to (0,0) in MoveWindow

def close_game_window(title):
    logging.info("[ENTER] close_game_window")
    whndl =  get_whndl(title)
    win32gui.PostMessage(whndl, win32con.WM_CLOSE, 0, 0)

def restart_game():
    logging.info("[ENTER] restart_game")
    whndl =  get_whndl("Hearthstone")
    if whndl != None and whndl != 0:
        #print 'got whndl Hearthstone'
        win32gui.ShowWindow(whndl, win32con.SW_RESTORE)
        foreground_whndl(whndl)
        pause_pensively(1)
        reset_game_window()
    else:
        whndl_error = get_whndl("Battle.net Error")
        if whndl_error == None or whndl_error == 0:
            #if get_hwnds().count('Battle.net') > 1:#client wants to restart
            #    #print 'got multiple whndl Battle.net'
            #    whndl  = get_whndl("Battle.net")
            #    #prepare battlenet window for input
            #    win32gui.ShowWindow(whndl, win32con.SW_MAXIMIZE)
            #    foreground_whndl(whndl)
            #    pause_pensively(30)
            #
            #    whndl = 0
            #else:
                #print 'got whndl Battle.net'
            whndl = get_whndl("Battle.net")

            if whndl != None and whndl != 0:
                #print 'got a whndl'
                #Maximize battlenet to full screen resolution and scale defines respectively
                defines.game_screen_res=defines.screen_box[2:]
                defines.window_box=defines.screen_box[2:]

                #prepare battlenet window for input
                win32gui.ShowWindow(whndl, win32con.SW_MAXIMIZE)
                foreground_whndl(whndl)
                pause_pensively(2)

                #try to start the game
                match_coord_games =  [170,50]
                match_coord_hs    =  [60,430]
                match_coord_play  =  [290,970]
                move_and_leftclick(match_coord_games)
                move_and_leftclick(match_coord_hs)
                move_and_leftclick(match_coord_play)

                #get battlenet out of the way
                pause_pensively(1)
                win32gui.ShowWindow(whndl, win32con.SW_MINIMIZE)
                pause_pensively(5)
                
                reset_game_window()

                game_whndl =  get_whndl("Hearthstone")

        else:
            foreground_whndl(whndl_error)
            pycwnd_error = make_pycwnd(whndl_error)
            pycwnd_click(pycwnd_error,defines.bnet_launch_error_button)

#return a list of all window titles
def get_hwnds():
  def callback (hwnd, hwnds):
    hwnds.append(win32gui.GetWindowText(hwnd))
    return True

  hwnds = []
  win32gui.EnumWindows(callback, hwnds)
  return hwnds
  
def main():
    pass

if __name__ == '__main__':
    main()