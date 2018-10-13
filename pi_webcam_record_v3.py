#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 09:13:00 2018

@author: Melody
"""

import numpy as np
import cv2
import scipy
#import argparse

def main():
    

    cap_0 = cv2.VideoCapture(0)
    cap_1 = cv2.VideoCapture(1)

    while(True):
        # Capture frame-by-frame
        ret_0, frame_0 = cap_0.read()
        ret_1, frame_1 = cap_1.read()
        
        frame_0 = scipy.misc.imresize(frame_0, 0.5)
        frame_1 = scipy.misc.imresize(frame_1, 0.5)
        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frame = np.concatenate((frame_0, frame_1), axis = 0)
    
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap_0.release()
    cap_1.release()
    cv2.destroyAllWindows()
    
main()
# if __name__== "__main__":      This is py27 version code.