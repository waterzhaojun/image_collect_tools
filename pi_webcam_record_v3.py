#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 09:13:00 2018

@author: Melody
"""

import numpy as np
import cv2
#import imutils
#import argparse

def main():

    width = 200
    height = 150

    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FPS, 1)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            
        else:
            print('Not ready')

#       Display the resulting frame
            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap_0.release()
    cap_1.release()
    cap_2.release()
    cap_3.release()
    cv2.destroyAllWindows()
    
main()
# if __name__== "__main__":      This is py27 version code.
