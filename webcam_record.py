#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 09:13:00 2018

@author: Melody
"""
import cv2
import datetime
#import imutils
import argparse

def main(videoname, fps, framesize, showVideo, port, resizeframe):
    
    # set file name
    if videoname is None:
        thedate = datetime.datetime.now().date().strftime('%Y%b%d')
        thetime = datetime.datetime.now().time().strftime('%H%M%S')
        videoname = thedate + '_' + thetime

    cap = cv2.VideoCapture(port)
    print(cv2.__version__)
    print(cap.get(cv2.CAP_PROP_FPS)) #查看这个video源的fps
    cap.set(cv2.CAP_PROP_FPS, 15) #重设这个video源的采集fps
    print(cap.get(cv2.CAP_PROP_FPS))
    # set frame width and height here won't change the output frame size
    # You have to resize it after create at below.
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, framesize[0])
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, framesize[1])
    
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(videoname+'.mov', fourcc, fps, framesize)
    
    
        
    
    # After create VideoWriter it will open by default.
    #out.open()

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        

        if ret:
            if resizeframe:
                frame = cv2.resize(frame, framesize)
            out.write(frame)

            if showVideo:
                
                cv2.imshow('frame',frame)
        else:
            print('Not ready')
            # break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
#main()
if __name__== "__main__":      #This is py27 version code.
    parser = argparse.ArgumentParser(description='record video')
    parser.add_argument('--videoname', default = None,
                        help='the name of the video')
    parser.add_argument('--fps', default = 10, type = int,
                        help='fps of the output video')
    parser.add_argument('--resizeframe', default = True, type = bool,
                        help='Whether resize the video frame')
    parser.add_argument('--framesize', default = (800,450), 
                        help='frame size')
    parser.add_argument('--showVideo', default = True, type = bool,
                        help = 'Whether show the video during recording')
    parser.add_argument('--port', default = 0, type = int,
                        help = 'webcam port')

    args = parser.parse_args()

    main(videoname=args.videoname, fps=args.fps, framesize = args.framesize,
         showVideo = args.showVideo, port = args.port, resizeframe = args.resizeframe)
