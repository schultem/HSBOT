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

H_BINS = 30
S_BINS = 32

#Default to take a screenshot of the whole screen
def screen_cap(box=defines.screen_box):
    src_PIL = ImageGrab.grab(defines.screen_box)
    src = np.array(src_PIL) 
    # Convert RGB to BGR 
    return src[:, :, ::-1].copy()

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

def pre_calculate_des(img_directory):
    # Initiate SIFT detector
    sift = SIFT()
    _, des2 = sift.detectAndCompute(img2,None)
    return des2

#provide two images and a minimum match count, return true for match, false for no match
def calc_sift(img1,img2):
    # Initiate SIFT detector
    sift = SIFT()
    
    # find the keypoints and descriptors with SIFT
    _, des1 = sift.detectAndCompute(img1,None)
    _, des2 = sift.detectAndCompute(img2,None)
    
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
def get_state_sift(src,descs):
    max_good = 0
    max_f = None

    for f in descs:
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

    _,falling_edges = vertical_edges(mask,mask.shape[0]/2)
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
        if falling_edges[i][0]-rising_edges[i][0] > min_threshold:
            if falling_edges[i][0]-rising_edges[i][0] < max_threshold:
                mid_edges.append([(rising_edges[i][0]+falling_edges[i][0])/2,rising_edges[i][1]])
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
    rising_edges,falling_edges = vertical_edges(mask,mask.shape[0]/2)#rising and falling edges of the minions
    mid_edges= get_mid_vertical_edges(rising_edges,falling_edges,min_threshold,max_threshold)#edges of the minions
    if mid_edges != None:
        mid_edges = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges]#translate coords to full screen coords rather than box coords
        #mid_edges_min = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges_min]
        #mid_edges_max = [[x+box[0],y+box[1]+pad] for [x,y] in mid_edges_max]
    else:
        mid_edges=[[x+box[0],y+box[1]+pad] for [x,y] in rising_edges]
    return mid_edges#,mid_edges_min,mid_edges_max

def save_img_box(src,box,filename='temp'):
    src_box = src[box[1]:box[3],box[0]:box[2]]
    imwrite(os.getcwd() + '\\'+filename+'.png', src_box)

def np_to_img(src):
    return cv.fromarray(src)

def img_to_np(src):
    return np.asarray(src[:,:])

