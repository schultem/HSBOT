import win32api, win32con
import time
import defines

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

def main():
    pass

if __name__ == '__main__':
    main()