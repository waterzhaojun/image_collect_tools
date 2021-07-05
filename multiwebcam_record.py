#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 14:39:35 2018

@author: Melody
"""

import cv2
import datetime
import argparse
import numpy as np
import math
import os
    

def main(savepath, fps, framesize, showVideo, portNum, passPortNum):
    
    # setting ========================================
    cols = 2 # How many cols show in the monitor.
    file_format = '.mov' # Output file type.
    fourcc = cv2.VideoWriter_fourcc('M','P','4','v')#('m','p','4','v') # compress code
    monitor_framesize = [int(framesize[0]/2), int(framesize[1]/2)] # the camera size showed in monitor. It could be different to save size.

    if passPortNum == None:
        ports = np.arange(portNum)
    else:
        ports = [x for x in np.arange(portNum + len(passPortNum)) if x not in passPortNum]

    rows = int(math.ceil(len(ports)/2))

    
    background = np.zeros(
        (int(monitor_framesize[1] * rows), int(monitor_framesize[0]*cols), 3), 
        np.uint8
    )
    print('Creating a monitor with %d webcam. Monitor size %d x %d' % (cols * rows, background.shape[0], background.shape[1]))

    # set file name
    if savepath is None:
        thedate = datetime.datetime.now().date().strftime('%Y-%m-%d')
        thetime = datetime.datetime.now().time().strftime('%H-%M-%S')
        savepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), thedate + ' ' + thetime)
    
    if not os.path.exists(savepath):
        os.mkdir(savepath)

    
    capDict = dict()
    
    # setup ports ====================================
    cams = []
    for i in range(len(ports)):
        # capDict['cap'+str(i)] = cv2.VideoCapture(i)

        videopath = os.path.join(savepath, 'port_' + str(ports[i]) + file_format)
        
        cams.append({
            'savepath': videopath,
            'videoSource': cv2.VideoCapture(ports[i]),
            'videoWriter': cv2.VideoWriter(videopath, fourcc, fps, framesize),
            'monitor_position_c': i % cols,
            'monitor_position_r': math.floor(i/cols)

        })

    # cap.set(cv2.CAP_PROP_FPS, 1)
    
    # set frame width and height here won't change the output frame size
    # You have to resize it after create at below.
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, framesize[0])
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, framesize[1])


    while(True):
        # Capture frame-by-frame
        for c in cams:
            ret, frame = c['videoSource'].read()
            frame = cv2.resize(frame, framesize)
            
            if ret:
                c['videoWriter'].write(frame)
                row0 = int(c['monitor_position_r'] * monitor_framesize[1])
                row1 = int((c['monitor_position_r'] + 1) * monitor_framesize[1])
                col0 = int(c['monitor_position_c'] * monitor_framesize[0])
                col1 = int((c['monitor_position_c'] + 1) * monitor_framesize[0])
                background[row0:row1, col0:col1,:] = cv2.resize(frame, monitor_framesize)
        
        #out.write(background)

        if showVideo:
            cv2.imshow('frame',background)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            tmp = input('If you are sure you want to stop recording, type "y" and press ENTER: ')
            if tmp.lower() == 'y':
                break
    
    # When everything done, release the capture
    print('Start to close cameras.')
    for c in cams:
        cams['videoSource'].release()
    cv2.destroyAllWindows()
    print('Recording finished.')
    
#main()

parser = argparse.ArgumentParser(description='record video')
parser.add_argument('--savepath', default = None,
                    help='It will build a folder and save videos from different sources in the folder.')
parser.add_argument('--fps', default = 30, type = int,
                    help='fps of the output video')
parser.add_argument('--framesize', default = (640, 480), # (480,270), 
                    help='The frame size of each webcam output image.')
parser.add_argument('--showVideo', default = True, type = bool,
                    help = 'Whether show the video during recording')
parser.add_argument('-n', '--portNum', default = 2, type = int,
                    help = 'webcam port')
parser.add_argument('-p', '--passPortNum', default = None, nargs = '*', type = int, help = 'If you want to pass some port, set an int here.')

args = parser.parse_args()

if __name__== "__main__":      #This is py27 version code.

    main(savepath=args.savepath, fps=args.fps, 
        framesize = args.framesize,
        showVideo = args.showVideo, 
        portNum = args.portNum, passPortNum = args.passPortNum
    )
