#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 09:13:00 2018

@author: Melody
"""

import cv2
#import imutils
import argparse

def main(videoname, fps, framesize, showVideo, port):

    cap = cv2.VideoCapture(port)
    # cap.set(cv2.CAP_PROP_FPS, 1)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    # fourcc = cv2.CV_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(videoname+'.mov', fourcc, fps, framesize)
    #out.open()

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.resize(frame, framesize)

        if ret:
            out.write(frame)

            if showVideo:
                
                cv2.imshow('frame',frame)
        else:
            print('Not ready')
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    
#main()
if __name__== "__main__":      #This is py27 version code.
    parser = argparse.ArgumentParser(description='record video')
    parser.add_argument('--videoname', default = 'new',
                        help='the name of the video')
    parser.add_argument('--fps', default = 10, type = int,
                        help='fps of the output video')
    parser.add_argument('--framesize', default = (200,100), 
                        help='frame size')
    parser.add_argument('--showVideo', default = False, type = bool,
                        help = 'Whether show the video during recording')
    parser.add_argument('--port', default = 0, type = int,
                        help = 'webcam port')

    args = parser.parse_args()

    main(videoname=args.videoname, fps=args.fps, framesize = args.framesize,
         showVideo = args.showVideo, port = args.port)
