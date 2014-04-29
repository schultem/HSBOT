#tested on python 2.7.6
from cv2 import * #version 2.4.6 for python 2.7
import ImageGrab  #PIL for python 2.7
import numpy as np#numpy for python 2.7
import os
import defines
from pytesser import *
from countdict import countdict

#HSV ranges of green/red bounding fires that surround playable cards/minions
#suffix _z is a wider range for masking colors over taunts
#suffix _cd is a smaller range for masking card attack/defense data
lower_green    = cv.Scalar(45, 100, 200)
upper_green    = cv.Scalar(80, 255, 255)
lower_green_z  = cv.Scalar(20, 50,  100)
upper_green_z  = cv.Scalar(70, 255, 255)
lower_green_cd = cv.Scalar(55, 240, 200)
upper_green_cd = cv.Scalar(65, 255, 255)
lower_red      = cv.Scalar(0,  130, 240)
upper_red      = cv.Scalar(20, 255, 255)
lower_red_z    = cv.Scalar(0,  50,  100)
upper_red_z    = cv.Scalar(23, 255, 255)
lower_red_cd   = cv.Scalar(0,  225, 225)
upper_red_cd   = cv.Scalar(10, 255, 255)
lower_white_cd = cv.Scalar(0,  0,   225)
upper_white_cd = cv.Scalar(1,  1,   255)
lower_white_cd_war  = cv.Scalar(9,   50,   100)
upper_white_cd_war  = cv.Scalar(12,  57,   255)
lower_white_cd_town = cv.Scalar(94,  18,   100)
upper_white_cd_town = cv.Scalar(100,  22,   255)

H_BINS = 30
S_BINS = 32

minion_font_mask = imread('images//minion_font_mask.png',0)

#Default to take a screenshot of the whole screen
def screen_cap(box=defines.screen_box):
    src_PIL = ImageGrab.grab(box)
    src = np.array(src_PIL) 
    # Convert RGB to BGR 
    return src[:, :, ::-1].copy()

def screen_save(box=defines.screen_box,filename='temp\\temp'):
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\'+filename+'.png', 'PNG')

def screen_load(filename='temp\\temp'):
    return imread(os.getcwd() + '\\'+filename+'.png',0)

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

#Earth Movers Distance comparison of histograms, use a precalculated sig of src2
def calc_emd_pre_calculated_src2(src1,sig2):
    h_bins = H_BINS
    s_bins = S_BINS

    hist1= calc_histogram(src1)

    numRows = h_bins*s_bins
    
    sig1 = cv.CreateMat(numRows, 3, cv.CV_32FC1)

    for h in range(h_bins):
        for s in range(s_bins): 
            bin_val = cv.QueryHistValue_2D(hist1, h, s)
            cv.Set2D(sig1, h*s_bins+s, 0, cv.Scalar(bin_val))
            cv.Set2D(sig1, h*s_bins+s, 1, cv.Scalar(h))
            cv.Set2D(sig1, h*s_bins+s, 2, cv.Scalar(s))

    return cv.CalcEMD2(sig1,sig2,cv.CV_DIST_L2)

#to speed up comparisons calculate the histogram for an image for use later
def pre_calculate_sig(src2):
    h_bins = H_BINS
    s_bins = S_BINS

    hist2= calc_histogram(src2)

    numRows = h_bins*s_bins
    
    sig2 = cv.CreateMat(numRows, 3, cv.CV_32FC1)
    
    for h in range(h_bins):
        for s in range(s_bins): 
    
            bin_val = cv.QueryHistValue_2D(hist2, h, s)
            cv.Set2D(sig2, h*s_bins+s, 0, cv.Scalar(bin_val))
            cv.Set2D(sig2, h*s_bins+s, 1, cv.Scalar(h))
            cv.Set2D(sig2, h*s_bins+s, 2, cv.Scalar(s))
    
    return sig2
        
#pre calculate the sigs of a directory and return as a dictionary
def get_sigs(min_directory):
    sigs={}
    for f in os.listdir(min_directory):
        sigs[f] = pre_calculate_sig(cv.LoadImage(min_directory + f))
    
    return sigs

#pre calculate the descreiptors of a directory and return as a dictionary
def get_descs(min_directory):
    sift = SIFT()
    descriptors={}
    for f in os.listdir(min_directory):
        _, des = sift.detectAndCompute(imread(min_directory + f),None)
        descriptors[f] = des

    return descriptors

def pre_calculate_des(img2):
    # Initiate SIFT detector
    sift = SIFT()
    _, des2 = sift.detectAndCompute(img2,None)
    return des2

#provide two images and a minimum match count, return true for match, false for no match
#return average match coordinates
def calc_sift(img1,img2,ratio=0.7):
    # Initiate SIFT detector
    sift = SIFT()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    
    flann = FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < ratio*n.distance:
            good.append(m)
            
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    #for pt in src_pts:
    x_pts = [pt[0][0] for pt in src_pts]
    y_pts = [pt[0][1] for pt in src_pts]
    
    if len(x_pts) and len(y_pts):
        match_coord=[int(np.average(x_pts)),int(np.average(y_pts))]
    else:
        match_coord=[0,0]

    return len(good),match_coord
    
#provide two images and a minimum match count, return true for match, false for no match
def calc_sift_precaculated_src2(src1,des2):
    # Initiate SIFT detector
    sift = SIFT()
    
    # find the keypoints and descriptors with SIFT
    _, des1 = sift.detectAndCompute(src1,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    
    flann = FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    
    return len(good)

    
#returns the most likely matching filename in an images directory
def get_image_info(src,sigs,box):
    min_emd = 9999999.99
    min_f = ''

    src = np_to_img(src)
    src_box = src[box[1]:box[3],box[0]:box[2]]
    for f in sigs:
        emd = calc_emd_pre_calculated_src2(src_box,sigs[f])
        if emd < min_emd:
            min_emd=emd
            min_f = f
    if min_f == None:
       return None
    else:
       return min_f[:-4]

#returns the most likely matching filename in an images directory
def get_image_info_sift(src,descs,box):
    max_good = 0
    max_f = None

    src_box = src[box[1]:box[3],box[0]:box[2]]
    for f in descs:
        good = calc_sift_precaculated_src2(src_box,descs[f])
        if good > max_good:
            max_good=good
            max_f = f
    if max_f == None:
       return None
    else:
       return max_f[:-4]

#returns the most likely matching filename in an images directory
def get_state(src,sigs):
    min_emd = 9999999.99
    min_f = ''
    src = np_to_img(src)

    for f in sigs:
        box = defines.c(defines.state_box[defines.state_dict[f[:-4]]])
        emd = calc_emd_pre_calculated_src2(src[box[1]:box[3],box[0]:box[2]],sigs[f])
        if emd < min_emd:
            min_emd=emd
            min_f = f
    return min_f[:-4]

#returns the most likely matching filename in an images directory
def get_state_sift(src,descs,ignore_list=[]):
    max_good = 0
    max_f = None

    for f in descs:
        if f not in ignore_list:
            box = defines.c(defines.state_box[defines.state_dict[f[:-4]]])
            good = calc_sift_precaculated_src2(src[box[1]:box[3],box[0]:box[2]],descs[f])
            if good > max_good:
                max_good=good
                max_f = f
    if max_f != None:
        return max_f[:-4]
    else:
        return None

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

def get_playable_cards(src,box,pad=20):
    src_box = src[box[1]:box[3],box[0]:box[2]]
    gray = cvtColor(src_box,COLOR_BGR2GRAY)
    result = inRange(gray,0, 0)
    hsv1 = cvtColor(src_box, COLOR_BGR2HSV)
    mask = inRange(hsv1,lower_green, upper_green)

    _,falling_edges = vertical_edges(mask)
    falling_edges = [[x+box[0]+pad,y+box[1]] for [x,y] in falling_edges]#translate coords to full screen coords rather than box coords
    return falling_edges

#return the middle egdes between rising and falling edges
#with an optional threshold rising to falling edge length
def get_mid_vertical_edges(rising_edges,falling_edges,min_threshold=0,max_threshold=200):
    if len(rising_edges) != len(falling_edges):
        return None

    mid_edges=[]
    #mid_edges_min=[]
    #mid_edges_max=[]
    for i in range(0,len(rising_edges)):
        if abs(falling_edges[i][0]-rising_edges[i][0]) > min_threshold:
            if abs(falling_edges[i][0]-rising_edges[i][0]) < max_threshold:
                mid_edges.append([(rising_edges[i][0]+falling_edges[i][0])/2,rising_edges[i][1]])
            else:
                mid_edges.append([(rising_edges[i][0]+35),rising_edges[i][1]])
        #    else:
        #        mid_edges_max.append([(rising_edges[i][0]+falling_edges[i][0])/2,rising_edges[i][1]])
        #else:
        #    mid_edges_min.append([(rising_edges[i][0]+falling_edges[i][0])/2,rising_edges[i][1]])
    return mid_edges#,mid_edges_min,mid_edges_max

def prepare_mask(src,color='green'):
    hsv1 = cvtColor(src, COLOR_BGR2HSV)
    if color=='green':
        mask = inRange(hsv1,lower_green, upper_green)
    elif color=='red':
        mask = inRange(hsv1,lower_red, upper_red)

    kernel = np.ones((1,1),np.uint8)
    opening = morphologyEx(mask, MORPH_OPEN, kernel)

    kernel = np.ones((5,5),np.uint8)
    dilation = dilate(opening,kernel,iterations = 2)

    return dilation

#Find occurrences of a color across a horizontal strip, add y-pad to the returned coordinates
def color_range_reduced_mids(src,box,color='green',pad=50,min_threshold=0,max_threshold=99999):
    src_box = src[box[1]:box[3],box[0]:box[2]]
    mask = prepare_mask(src_box,color)
    rising_edges,falling_edges = vertical_edges(mask)#rising and falling edges of the minions
    mid_edges= get_mid_vertical_edges(rising_edges,falling_edges,min_threshold,max_threshold)#edges of the minions
    if mid_edges != None:
        mid_edges = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges]#translate coords to full screen coords rather than box coords
        #mid_edges_min = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges_min]
        #mid_edges_max = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges_max]
    else:
        mid_edges=[[x+box[0],y+box[1]+pad] for [x,y] in rising_edges]
    return mid_edges#,mid_edges_min,mid_edges_max

def get_minions(src,box,pad=-50,min_threshold=25):
    foreground = src[box[1]:box[3],box[0]:box[2]]
    fg_hsv = cvtColor(foreground, COLOR_BGR2HSV)

    foreground_red_mask = inRange(fg_hsv,lower_red_z, upper_red_z)
    kernel = np.ones((1,1),np.uint8)
    foreground_red_mask = dilate(foreground_red_mask,kernel,iterations = 1)
    bitwise_not(foreground_red_mask, foreground_red_mask)
    #imwrite("tempmask.png",foreground_red_mask)

    kernel = np.ones((10,10),np.uint8)
    foreground_red_mask = morphologyEx(foreground_red_mask, MORPH_CLOSE, kernel)
    #imwrite("tempmaskclosed.png",foreground_red_mask)
    #imwrite("tempmasksrc.png",src)

    rising_edges,falling_edges = vertical_edges(foreground_red_mask)
    #print rising_edges,falling_edges
    mid_edges= get_mid_vertical_edges(rising_edges,falling_edges,min_threshold=min_threshold)
    if mid_edges != None:
        mid_edges = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges]
    else:
        mid_edges=[[x+box[0],y+box[1]+pad] for [x,y] in rising_edges]

    return mid_edges

#return the location of enemy taunt minions using subtractive background masking
def get_taunt_minions(src,box,pad=-50):
    background = imread('images//back.png')
    foreground = src[box[1]:box[3],box[0]:box[2]]
    background = resize(background, (foreground.shape[1],foreground.shape[0]))

    fg_hsv = cvtColor(foreground, COLOR_BGR2HSV)

    foreground_green_mask = inRange(fg_hsv,lower_green_z, upper_green_z)
    kernel = np.ones((5,5),np.uint8)
    foreground_green_mask = dilate(foreground_green_mask,kernel,iterations = 1)
    bitwise_not(foreground_green_mask, foreground_green_mask)

    foreground_red_mask = inRange(fg_hsv,lower_red_z, upper_red_z)
    kernel = np.ones((1,1),np.uint8)
    foreground_red_mask = dilate(foreground_red_mask,kernel,iterations = 1)
    bitwise_not(foreground_red_mask, foreground_red_mask)

    fgbg = BackgroundSubtractorMOG()
    fgmask = fgbg.apply(background)
    fgmask = fgbg.apply(foreground)

    fgmask = bitwise_and(foreground_green_mask, fgmask)
    fgmask = bitwise_and(foreground_red_mask, fgmask)

    kernel = np.ones((5,5),np.uint8)
    fgmask = morphologyEx(fgmask, MORPH_CLOSE, kernel)

    rising_edges,falling_edges = vertical_edges(fgmask)
    mid_edges= get_mid_vertical_edges(rising_edges,falling_edges)
    if mid_edges != None:
        mid_edges = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges]
    else:
        mid_edges=[[x+box[0],y+box[1]+pad] for [x,y] in rising_edges]
    return mid_edges

def read_minion_number_data(src,box=None,stage=None):
    global minion_font_mask
    if box==None:
        src_box=src
    else:
        src_box = src[box[1]:box[3],box[0]:box[2]]
    hsv = cvtColor(src_box, COLOR_BGR2HSV)

    minion_font_mask = resize(minion_font_mask, (hsv.shape[1],hsv.shape[0]))

    green_mask       = inRange(hsv,lower_green_cd, upper_green_cd)
    red_mask         = inRange(hsv,lower_red_cd, upper_red_cd)
    if stage in [None,'jungle','china']:
        white_mask       = inRange(hsv,lower_white_cd, upper_white_cd)
    elif stage=='war':
        white_mask       = inRange(hsv,lower_white_cd_war, upper_white_cd_war)
    elif stage=='town':
        white_mask       = inRange(hsv,lower_white_cd_town, upper_white_cd_town)
    else:
        white_mask       = inRange(hsv,lower_white_cd, upper_white_cd)

    total_mask       = bitwise_or(green_mask, red_mask)
    total_mask       = bitwise_or(total_mask, white_mask)
    total_mask       = bitwise_or(total_mask, minion_font_mask)

    #imwrite(os.getcwd() + '\\temp1.png', src_box)
    #imwrite(os.getcwd() + '\\temp5.png', total_mask)
    
    #convert opencv black and white np to PIL image
    total_mask = np_to_img(total_mask)
    im = Image.fromstring("L", cv.GetSize(total_mask), total_mask.tostring())
    
    #ocr
    text = image_to_string(im)
    #print text
    #remove non numeric chars

    txt_filter=""
    for ch in text:
        if ch=="X":#special character used in minion_font_mask
            txt_filter+=" "
        if ch=="x":#special character used in minion_font_mask
            txt_filter+=" "
        if ch=="I":
            txt_filter+="1"
        elif ch=="l":
            txt_filter+="1"
        elif ch=="!":
            txt_filter+="1"
        elif ch=="|":
            txt_filter+="1"
        elif ch=="o":
            txt_filter+="0"
        elif ch=="O":
            txt_filter+="0"
        elif ch=="?":
            txt_filter+="2"
        elif ch=="S":
            txt_filter+="8"
        elif ch=="s":
            txt_filter+="8"
        elif ch=="z":
            txt_filter+="2"
        elif ch=="Z":
            txt_filter+="2"
        elif ch.isdigit():
            txt_filter+=ch
        else:
            txt_filter+=' '

    return txt_filter

def get_minion_data(box,stage):
    potential_data=[]
    pd_cnt=0
    for i in range(0,100):
    
        #src_data = imread('Hearthstone_Screenshot_4.19.2014.14.59.36.png')
        #src      = src_data[box[1]:box[3],box[0]:box[2]]
        src = screen_cap(box=box)
        player_minion_data=read_minion_number_data(src,stage=stage).split()
        #print player_minion_data
        for pdata in player_minion_data:
            if int(pdata) > 20:#chances are there won't be minions with more than 20 attack
                player_minion_data_revised=[]
                for pdata_new in player_minion_data:
                    if int(pdata_new) > 20:
                        for ch in pdata_new:
                            player_minion_data_revised.append(ch)
                    else:
                        player_minion_data_revised.append(pdata_new)
                player_minion_data=player_minion_data_revised
                break
               
        if len(player_minion_data)%2==0:
            if potential_data == player_minion_data:
                pd_cnt+=1
                if pd_cnt==3:
                    return potential_data
            else:
                pd_cnt=0
                potential_data = player_minion_data
    
    return None

def read_white_data(src,box):
    if box==None:
        src_box=src
    else:
        src_box = src[box[1]:box[3],box[0]:box[2]]
    hsv = cvtColor(src_box, COLOR_BGR2HSV)

    white_mask       = inRange(hsv,lower_white_cd, upper_white_cd)

    src_mask_img = np_to_img(white_mask)
    im = Image.fromstring("L", cv.GetSize(src_mask_img), src_mask_img.tostring())
    
    #ocr
    text = image_to_string(im)

    txt_filter=""
    for ch in text:
        if ch=="I":
            txt_filter+="1"
        elif ch=="l":
            txt_filter+="1"
        elif ch=="!":
            txt_filter+="1"
        elif ch=="|":
            txt_filter+="1"
        elif ch=="(":
            txt_filter+="1"
        elif ch==")":
            txt_filter+="1"
        elif ch=="{":
            txt_filter+="1"
        elif ch=="}":
            txt_filter+="1"
        elif ch=="Y":
            txt_filter+="1"
        elif ch=="[":
            txt_filter+="0"
        elif ch=="o":
            txt_filter+="0"
        elif ch=="O":
            txt_filter+="0"
        elif ch=="0":
            txt_filter+="0"
        elif ch=="?":
            txt_filter+="2"
        elif ch=="S":
            txt_filter+="8"
        elif ch=="s":
            txt_filter+="8"
        elif ch=="z":
            txt_filter+="2"
        elif ch=="Z":
            txt_filter+="2"
        elif ch.isdigit():
            txt_filter+=ch
        else:
            txt_filter+=''

    return txt_filter

    
def minion_data_mask(src,box,stage):
    if box==None:
        src_box=src
    else:
        src_box = src[box[1]:box[3],box[0]:box[2]]
    hsv = cvtColor(src_box, COLOR_BGR2HSV)

    green_mask       = inRange(hsv,lower_green_cd, upper_green_cd)
    red_mask         = inRange(hsv,lower_red_cd, upper_red_cd)
    if stage in [None,'jungle','china']:
        white_mask       = inRange(hsv,lower_white_cd, upper_white_cd)
    elif stage=='war':
        white_mask       = inRange(hsv,lower_white_cd_war, upper_white_cd_war)
    elif stage=='town':
        white_mask       = inRange(hsv,lower_white_cd_town, upper_white_cd_town)
    else:
        white_mask       = inRange(hsv,lower_white_cd, upper_white_cd)

    total_mask = bitwise_or(green_mask, red_mask)
    total_mask = bitwise_or(total_mask, white_mask)
    #imwrite('test2.png',white_mask)
    #imwrite('test3.png',total_mask)
    #imwrite('test4.png',hsv)
    return total_mask

def minion_data_to_string(src_mask):
    #convert opencv black and white np to PIL image
    src_mask_img = np_to_img(src_mask)
    im = Image.fromstring("L", cv.GetSize(src_mask_img), src_mask_img.tostring())
    
    #ocr
    text = image_to_string(im)
    #print text
    #imwrite('test.png',src_mask)
    if '-1' in text:
        text="4"
    #remove non numeric chars
    txt_filter=""
    for ch in text:
        if ch=="I":
            txt_filter+="1"
        elif ch=="l":
            txt_filter+="1"
        elif ch=="!":
            txt_filter+="1"
        elif ch=="|":
            txt_filter+="1"
        elif ch=="(":
            txt_filter+="1"
        elif ch==")":
            txt_filter+="1"
        elif ch=="{":
            txt_filter+="1"
        elif ch=="}":
            txt_filter+="1"
        elif ch=="Y":
            txt_filter+="1"
        elif ch=="[":
            txt_filter+="0"
        elif ch=="o":
            txt_filter+="0"
        elif ch=="O":
            txt_filter+="0"
        elif ch=="0":
            txt_filter+="0"
        elif ch=="?":
            txt_filter+="2"
        elif ch=="S":
            txt_filter+="8"
        elif ch=="s":
            txt_filter+="8"
        elif ch=="z":
            txt_filter+="2"
        elif ch=="Z":
            txt_filter+="2"
        elif ch.isdigit():
            txt_filter+=ch
        else:
            txt_filter+=' '

    return txt_filter

def get_minion_data_split(boxes,stage):
    potential_data = []
    result_data    = []
    
    for box in boxes:
        c_box = defines.c(box) #get a new reference so the defines list isn't permanently changed
        potential_data.append([])
        for src_pass in range(0,20):
            #print c_box
            src = screen_cap(box=c_box)
            mask_result = minion_data_mask(src,None,stage)
            txt_result  = minion_data_to_string(mask_result)

            try:
                potential_data[-1].append(int(txt_result))
            except:
                potential_data[-1].append(' ')

            potential_mode = countdict(potential_data[-1],limit=5)

            if potential_mode >= 0:
                if potential_data[-1][-1] != '':
                    result_data.append(potential_data[-1][-1])
                    break

    return result_data

#return a dict of all minion data given a data box, a minion box, and a taunt box
#do not defines.c(minion_data_boxes), it is a list of boxes, so it would get permanently changed.
#Instead get_minion_data_split takes care of the conversion
def all_minion_data(src,minion_data_boxes,minions_box,minions_box_taunts_reduced=None,minions_box_taunts=None,minions_box_playable=None,stage=None,reduced_color=None):
    minion_coords = get_minions(src,minions_box)
    #print minion_coords
    #cull minion data not close to known minion coords to save time
    culled_minion_data_boxes = []
    for box in minion_data_boxes:
        c_box = defines.c(box) #get a new reference so the defines list isn't permanently changed
        for minion_coord in minion_coords:
            if abs((c_box[0]+c_box[2])/2 - minion_coord[0]) <= 50:
                culled_minion_data_boxes.append(box)
                break
    #print culled_minion_data_boxes
    minion_data=get_minion_data_split(culled_minion_data_boxes,stage)
    #print minion_data
    if minions_box_taunts!=None:
        minion_taunts = get_taunt_minions(src,minions_box_taunts)
    else:
        minion_taunts=[]
    #print minion_taunts
    if minions_box_taunts_reduced!=None and reduced_color!=None:
        minion_taunts_reduced = color_range_reduced_mids(src,minions_box_taunts_reduced,color=reduced_color,min_threshold=90,max_threshold=200)
    else:
        minion_taunts_reduced=[]
    #print minion_taunts_reduced
    
    minion_taunts.extend(minion_taunts_reduced)
    
    if minions_box_playable!=None:
        minions_playable = color_range_reduced_mids(src,minions_box_playable,color='green',min_threshold=45,max_threshold=200)
    else:
        minions_playable=[]
    #print minions_playable

    minions = []
    minion_ad=0
    for coord in minion_coords:
        minion={}
        minion['coord'] = coord

        if len(minion_taunts):
            min_coord=9999
            for t_coord in minion_taunts:
                if (abs(t_coord[0]-coord[0]) < min_coord):
                    min_coord=abs(t_coord[0]-coord[0])
            if min_coord<30:
                minion['taunt'] = True
            else:
                minion['taunt'] = False
        else:
            minion['taunt'] = False

        if len(minions_playable):
            min_coord=9999
            for t_coord in minions_playable:
                if (abs(t_coord[0]-coord[0]) < min_coord):
                    min_coord=abs(t_coord[0]-coord[0])
            if min_coord<30:
                minion['playable'] = True
            else:
                minion['playable'] = False
        else:
            minion['playable'] = False

        minions.append(minion)
        minion_ad+=1

    if minion_data != None:
        if len(minion_data) == 2*len(minions):
            if len(minion_data):
                for i in range(0,len(minion_coords)):
                    minions[i]['attack']  = minion_data[2*i]
                    minions[i]['defense'] = minion_data[2*i+1]

    return minions

def save_img_box(src,box=None,filename='temp'):
    if box==None:
        src_box=src
    else:
        src_box = src[box[1]:box[3],box[0]:box[2]]
    imwrite(os.getcwd() + '\\'+filename+'.png', src_box)

def np_to_img(src):
    return cv.fromarray(src)

def img_to_np(src):
    return np.asarray(src[:,:])

