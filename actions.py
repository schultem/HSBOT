import win32api, win32con, win32gui, win32ui, win32process
import time
import defines
from pw import pw

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	
def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)

def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)

def setCursorPos(coord):
    win32api.SetCursorPos((coord[0],coord[1]))

def getCursorPos():
    x,y = win32api.GetCursorPos()
    return [x,y]

def interpCursorPos(coord):
    coord_curr = getCursorPos()
    while(coord_curr[0]!=coord[0] or coord_curr[1]!=coord[1]):        
        coord_curr = getCursorPos()
        for i in range(0,15000):    #pause
            i=i+1
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
        setCursorPos([coord_curr[0]+xd,coord_curr[1]+yd])

def pause_pensively(s):
    time.sleep(s)

def leftclick_drag_and_release(click_coord, release_coord):
    interpCursorPos(click_coord)
    leftDown()
    interpCursorPos(release_coord)
    leftUp()

def leftclick_move_and_leftclick(click_coord, click_coord_2):
    interpCursorPos(click_coord)
    leftClick()
    interpCursorPos(click_coord_2)
    leftClick()

def move_and_leftclick(click_coord):
    interpCursorPos(click_coord)
    leftClick()

def move_cursor(move_coord):
    interpCursorPos(move_coord)

def get_whndl(window_name):
    whndl = win32gui.FindWindowEx(0, 0, None, window_name)
    return whndl

def make_pycwnd(hwnd):       
    PyCWnd = win32ui.CreateWindowFromHandle(hwnd)
    return PyCWnd

def pycwnd_click(pycwnd,coord):
    lParam = coord[1] << 16 | coord[0]
    pycwnd.PostMessage(win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam);
    pause_pensively(0.1)
    pycwnd.PostMessage(win32con.WM_LBUTTONUP, 0, lParam);
    pause_pensively(0.1)

def foreground_whndl(whwnd):
    win32gui.SetForegroundWindow(whwnd)

def pycwnd_string(pycwnd, msg):
    for c in msg:
        if c == "\n":
            pycwnd.SendMessage(win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            pycwnd.SendMessage(win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        else:
            pause_pensively(0.3)
            pycwnd.SendMessage(win32con.WM_CHAR, ord(c), 0)
    #pycwnd.UpdateWindow()

def whnds_to_text(hwnds):
    for hwnd in range(0,len(hwnds)):
        hwnds[hwnd]=win32gui.GetWindowText(hwnds[hwnd])
    return hwnds

def print_all_whnds(hwnds):
    hwnds=[]
    def enumHandler(hwnd, lParam):
        hwnds.append(hwnd)

    win32gui.EnumWindows(enumHandler, None)
    text_hwnds = whnds_to_text(hwnds)
    print text_hwnds

#Return True if game is not minimized and is running.  Otherwise False
def check_game():
    whndl =  get_whndl("Hearthstone")
    if whndl != None and whndl != 0:
        #win32gui.IsWindowVisible(whndl)
        return True
    return False

def restart_game():
    whndl =  get_whndl("Hearthstone")
    if whndl != None and whndl != 0:
        win32gui.ShowWindow(whndl, win32con.SW_MAXIMIZE)
        pause_pensively(10)
    else:
        whndl_error = get_whndl("Battle.net Error")
        if whndl_error == None or whndl_error == 0:
            whndl  = get_whndl("Battle.net")
            if whndl != None and whndl != 0:
                #prepare battlenet window for input
                win32gui.ShowWindow(whndl, win32con.SW_MAXIMIZE)
                foreground_whndl(whndl)
                pycwnd = make_pycwnd(whndl)
            
                #try to log on again
                pycwnd_click(pycwnd,defines.c(defines.bnet_go_online_button))
                whndl_login = get_whndl("Battle.net Login")
                if whndl_login != None and whndl_login != 0:
                    #prepare battlenet login window for input
                    pycwnd_login = make_pycwnd(whndl_login)
                    pycwnd_string(pycwnd_login,pw)
                    pycwnd_click(pycwnd_login,defines.bnet_accept_pw_button)
                    pause_pensively(5)
            
                #try to start the game
                pycwnd_click(pycwnd,defines.c(defines.bnet_hearthstone_button))
                pycwnd_click(pycwnd,defines.c(defines.bnet_play_button))
            
                #get battlenet out of the way
                pause_pensively(5)
                win32gui.ShowWindow(whndl, win32con.SW_MINIMIZE)
                pause_pensively(20)
        else:
            foreground_whndl(whndl_error)
            pycwnd_error = make_pycwnd(whndl_error)
            pycwnd_click(pycwnd_error,defines.bnet_launch_error_button)

def main():
    pass

if __name__ == '__main__':
    main()