#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:39:35 2018

@author: Melody
"""

import cv2
import datetime
#import imutils
import argparse
import numpy as np
import math
    

def main(videoname, fps, framesize, showVideo, portNum):
    
    cols = 2
    rows = int(math.ceil(portNum/2))
    
    framecol = framesize[0]
    framerow = framesize[1]
    
    background = np.zeros((int(framerow*rows), int(framecol*cols), 3), np.uint8)
    print(background.shape)
    print(cols, rows)
    # set file name
    if videoname is None:
        thedate = datetime.datetime.now().date().strftime('%Y%b%d')
        thetime = datetime.datetime.now().time().strftime('%H%M%S')
        videoname = thedate + '_' + thetime
    
    capDict = dict()
    
    for i in range(portNum):
        capDict['cap'+str(i)] = cv2.VideoCapture(i)

    # cap.set(cv2.CAP_PROP_FPS, 1)
    
    # set frame width and height here won't change the output frame size
    # You have to resize it after create at below.
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, framesize[0])
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, framesize[1])
    
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(videoname+'.mov', fourcc, fps, 
                          (background.shape[1], background.shape[0]))


    while(True):
        # Capture frame-by-frame
        for i in range(portNum):
            ret, frame = capDict['cap'+str(i)].read()
            frame = cv2.resize(frame, framesize)
            present_col = i%cols
            present_row = math.floor(i/cols)
            if ret:
                row0 = int(present_row*framerow)
                row1 = int((present_row+1)*framerow)
                col0 = int(present_col*framecol)
                col1 = int((present_col+1)*framecol)
                background[row0:row1, col0:col1,:]=frame
        
        out.write(background)

        if showVideo:
                
            cv2.imshow('frame',background)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    for i in range(portNum):
        capDict['cap'+str(i)].release()
    cv2.destroyAllWindows()
    
#main()
if __name__== "__main__":      #This is py27 version code.
    parser = argparse.ArgumentParser(description='record video')
    parser.add_argument('--videoname', default = None,
                        help='the name of the video')
    parser.add_argument('--fps', default = 10, type = int,
                        help='fps of the output video')
    parser.add_argument('--framesize', default = (480,270), 
                        help='The frame size of each webcam output image.')
    parser.add_argument('--showVideo', default = True, type = bool,
                        help = 'Whether show the video during recording')
    parser.add_argument('--portNum', default = 2, type = int,
                        help = 'webcam port')

    args = parser.parse_args()

    main(videoname=args.videoname, fps=args.fps, framesize = args.framesize,
         showVideo = args.showVideo, portNum = args.portNum)
