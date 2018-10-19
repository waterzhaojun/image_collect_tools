#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:14:47 2018

@author: Melody
"""

import cv2
import os
import numpy as np
import argparse

def main(videopath, imageNum, period, extract_method):

    # create folder
    folderpath = os.path.dirname(videopath)
    filename = os.path.basename(videopath).split('.')[0]
    newfolder = os.path.join(folderpath, filename)
    if not os.path.exists(newfolder):
        os.mkdir(newfolder)
    else:
        print('The output folder already exist. Do not need to create.')

    # load Video
    cap = cv2.VideoCapture(videopath)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if period is not None:
        period = np.multiply(period, fps*60).astype(int)
        period = np.array([np.maximum(0, period[0]), np.minimum(length, period[1])])
    else:
        period = [0, length]
    
    if extract_method == 'equal':
        idxes = np.linspace(period[0], period[1], imageNum)
    elif extract_method == 'random':
        idxes = np.random.choice(np.arange(period[0], period[1]), imageNum)
    else:
        raise ValueError('Please confirm your extract method')
        
    
    for i in idxes:
        msid = int(i/fps*1000)
        print('%s done' % msid)

        # cap.set(1, i) # 1 means CV_CAP_PROP_POS_FRAMES, check the list at 
        # https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set
        cap.set(0, msid)
        ret, frame = cap.read()
        
        if ret:
            filename = os.path.join(newfolder, str(msid)+'.jpg')
            cv2.imwrite(filename, frame)

    cap.release()
    cv2.destroyAllWindows()
    
if __name__== "__main__":      #This is py27 version code.
    parser = argparse.ArgumentParser(description='record video')
    parser.add_argument('--videopath', required = True,
                        help='the path of the video')
    parser.add_argument('--imageNum', default = 10, type = int,
                        help='The number of images need to extract from video.')
    parser.add_argument('--period', default = None, 
                        help='The period we want to extract images')
    parser.add_argument('--extract_method', default = 'equal', 
                        help = 'The way to extract images, either equal gap or random')


    args = parser.parse_args()

    main(videopath=args.videopath, imageNum=args.imageNum, 
         period=args.period, extract_method=args.extract_method)