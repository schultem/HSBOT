#tested on python 2.7.6
from cv2 import * #version 2.4.6 for python 2.7
import ImageGrab  #PIL for python 2.7
import numpy as np#numpy for python 2.7
import os
import defines

#HSV ranges of green/red bounding fires that surround playable cards/minions
lower_green = cv.Scalar(45, 100, 200)
upper_green = cv.Scalar(80, 255, 255)
lower_red   = cv.Scalar(0, 130, 240)
upper_red   = cv.Scalar(20, 255, 255)

H_BINS = 30 #hue
S_BINS = 32 #saturation

def screen_save(box=defines.screen_box,filename='temp\\temp'):
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\'+filename+'.png', 'PNG')

def screen_load(filename='temp\\temp'):
    return imread(os.getcwd() + '\\'+filename+'.png')

def calc_histogram(src):
    # Convert to HSV
    hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
    cv.CvtColor(src, hsv, cv.CV_BGR2HSV)

    # Extract the H and S planes
    size = cv.GetSize(src)
    h_plane = cv.CreateMat(size[1], size[0], cv.CV_8UC1)
    s_plane = cv.CreateMat(size[1], size[0], cv.CV_8UC1)
    cv.Split(hsv, h_plane, s_plane, None, None)
    planes = [h_plane, s_plane]

    #Define numer of bins
    h_bins = H_BINS
    s_bins = S_BINS

    #Define histogram size
    hist_size = [h_bins, s_bins]

    # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
    h_ranges = [0, 180]

    # saturation varies from 0 (black-gray-white) to 255 (pure spectrum color)
    s_ranges = [0, 255]

    ranges = [h_ranges, s_ranges]

    #Create histogram
    hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)

    #Calc histogram
    cv.CalcHist([cv.GetImage(i) for i in planes], hist)

    cv.NormalizeHist(hist, 1.0)

    #Return histogram
    return hist

#Earth Movers Distance comparison of histograms
def calc_emd(src1,src2):
    h_bins = H_BINS
    s_bins = S_BINS

    hist1= calc_histogram(src1)
    hist2= calc_histogram(src2)

    numRows = h_bins*s_bins
    
    sig1 = cv.CreateMat(numRows, 3, cv.CV_32FC1)
    sig2 = cv.CreateMat(numRows, 3, cv.CV_32FC1)    
    
    for h in range(h_bins):
        for s in range(s_bins): 
            bin_val = cv.QueryHistValue_2D(hist1, h, s)
            cv.Set2D(sig1, h*s_bins+s, 0, cv.Scalar(bin_val))
            cv.Set2D(sig1, h*s_bins+s, 1, cv.Scalar(h))
            cv.Set2D(sig1, h*s_bins+s, 2, cv.Scalar(s))
    
            bin_val = cv.QueryHistValue_2D(hist2, h, s)
            cv.Set2D(sig2, h*s_bins+s, 0, cv.Scalar(bin_val))
            cv.Set2D(sig2, h*s_bins+s, 1, cv.Scalar(h))
            cv.Set2D(sig2, h*s_bins+s, 2, cv.Scalar(s))

    return cv.CalcEMD2(sig1,sig2,cv.CV_DIST_L2)

#calculate the minimum emd file f compared to src
def calc_min_emd(src,min_directory):
    min_emd = 9999999.99
    min_f = ''
    for f in os.listdir(min_directory):
        emd = calc_emd(src,cv.LoadImage(min_directory + f))
        if emd < min_emd:
            min_emd = emd
            min_f=f
    if min_emd > 20:
        return None,None
    else:
        return min_f,min_emd

#returns the most likely matching filename in an images directory
def get_image_info(directory,src,box):
    directory = os.getcwd()+ '\\images\\' + directory + '\\'
    src = np_to_img(src)

    min_f,_ = calc_min_emd(src[box[1]:box[3],box[0]:box[2]],directory)
    if min_f !=None:
        return min_f[:-4]
    else:
        return None

#returns the most likely matching filename in an images directory
def get_state(src):
    directory = os.getcwd()+ '\\images\\state\\'
    min_emd = 9999999.99
    min_f = ''
    src = np_to_img(src)

    for f in os.listdir(directory):
        #print f
        box = defines.state_box[defines.state_dict[f[:-4]]]
        emd = calc_emd(src[box[1]:box[3],box[0]:box[2]],cv.LoadImage(directory + f))
        if emd < min_emd:
            min_emd=emd
            min_f = f
    return min_f[:-4]

#detect rising and falling edges across a binary image at y
def vertical_edges(image,y=None):
    if y == None:
        y = image.shape[0]/2
    
    rising_edges=[]
    falling_edges=[]
    for i in range(0,image.shape[1]-1):
        if image[y,i] < image[y,i+1]:
            rising_edges.append([i+1,y])
        elif image[y,i] > image[y,i+1]:
            falling_edges.append([i,y])
    
    return rising_edges,falling_edges 

#detect rising and falling edges across a binary image at x
def horizontal_edges(image,x=None):
    if x == None:
        x = image.shape[1]/2

    rising_edges=[]
    falling_edges=[]
    for i in range(0,image.shape[0]-1):
        if image[i,x] < image[i+1,x]:
            rising_edges.append([x,i+1])
        elif image[i,x] > image[i+1,x]:
            falling_edges.append([x,i])
    
    return rising_edges,falling_edges 

#Draw (approximately) vertical lines detected in an image to result
def draw_vertical_lines(src,result):
    vertical_lines = HoughLines(src,3,np.pi/180,100)
    if vertical_lines != None:
        for rho,theta in vertical_lines[0]:
            if theta > 2.6 or theta < 0.3:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                line(result,(x1,y1),(x2,y2),(255,255,255),3)
    return result

def get_playable_cards(src,box,pad=15):
    lower_green = cv.Scalar(45, 50, 150)#selects the green glow that surrounds playable cards
    upper_green = cv.Scalar(80, 255, 255)

    src_box = src[box[1]:box[3],box[0]:box[2]]
    gray = cvtColor(src_box,COLOR_BGR2GRAY)
    result = inRange(gray,0, 0)
    hsv1 = cvtColor(src_box, COLOR_BGR2HSV)
    mask = inRange(hsv1,lower_green, upper_green)
    lines = draw_vertical_lines(mask,result)
    
    _,falling_edges = vertical_edges(lines,lines.shape[0]/2)
    falling_edges = [[x+box[0]+pad,y+box[1]] for [x,y] in falling_edges]#translate coords to full screen coords rather than box coords
    
    return falling_edges

#return the middle egdes between rising and falling edges
def get_mid_vertical_edges(rising_edges,falling_edges):
    if len(rising_edges) != len(falling_edges):
        return None
    
    mid_edges=[]
    for i in range(0,len(rising_edges)):
        mid_edges.append([(rising_edges[i][0]+falling_edges[i][0])/2,rising_edges[i][1]])
    
    return mid_edges
    
#return the x center points between a list of x-ordered coordinates
def get_x_midpoints(mid_edges):
    midpoints=[]
    for i in range(0,len(mid_edges)-1):
        midpoints.append([(mid_edges[i][0]+mid_edges[i+1][0])/2,mid_edges[i][1]])
    return midpoints

def prepare_mask(src,color='green'):
    hsv1 = cvtColor(src, COLOR_BGR2HSV)
    if color=='green':
        mask = inRange(hsv1,lower_green, upper_green)
    elif color=='red':
        mask = inRange(hsv1,lower_red, upper_red)

    kernel = np.ones((2,2),np.uint8)
    opening = morphologyEx(mask, MORPH_OPEN, kernel)

    kernel = np.ones((10,10),np.uint8)
    dilation = dilate(opening,kernel,iterations = 2)

    return dilation

def color_range_mids(src,box,color='green'):
    src_box = src[box[1]:box[3],box[0]:box[2]]
    mask = prepare_mask(src_box,color)

    rising_edges,falling_edges = vertical_edges(mask,mask.shape[0]/2)#rising and falling edges of the minions
    mid_edges = get_mid_vertical_edges(rising_edges,falling_edges)#edges of the minions
    if mid_edges != None:
        mids  = get_x_midpoints(mid_edges)#center of the minions
        #verify that a center of a minion is playable by checking that the edges are connected
        verified_mids = []
        for i in range(0,len(mids)):
            rising_edges,falling_edges = horizontal_edges(mask,mids[i][0])
            if len(rising_edges) != 0 or len(falling_edges) != 0:
                verified_mids.append(mids[i])
        
        verified_mids = [[x+box[0],y+box[1]] for [x,y] in verified_mids]#translate coords to full screen coords rather than box coords
        return verified_mids
    else:
        return None

def color_range_reduced_mids(src,box,color='green',pad=70):
    src_box = src[box[1]:box[3],box[0]:box[2]]
    mask = prepare_mask(src_box,color)
    rising_edges,falling_edges = vertical_edges(mask,mask.shape[0]/2)#rising and falling edges of the minions
    mid_edges = get_mid_vertical_edges(rising_edges,falling_edges)#edges of the minions
    if mid_edges != None:
        mid_edges = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges]#translate coords to full screen coords rather than box coords
    else:
        mid_edges=[[x+box[0],y+box[1]+pad] for [x,y] in rising_edges]

    return mid_edges

def save_img_box(src,box,filename='temp'):
    src_box = src[box[1]:box[3],box[0]:box[2]]
    imwrite(os.getcwd() + '\\'+filename+'.png', src_box)

def np_to_img(src):
    return cv.fromarray(src)

def img_to_np(src):
    return np.asarray(src[:,:])

