#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 23:51:07 2018

@author: Melody
"""

import face_recognition
import cv2
import argparse
import os


def main(path):
    files = os.listdir(path)
    files = [x for x in files if x[-3:] in ['jpg', 'JPG']]
    
    for file in files:
        
        image = cv2.imread(os.path.join(path, file))
        face_locations = face_recognition.face_locations(image)
        if len(face_locations)>0:
            for i in range(len(face_locations)):
                coo = face_locations[i]
                face = image[coo[0]:coo[2], coo[3]:coo[1], :]
                
                face_folder = path+'_face'
                
                
                if not os.path.exists(face_folder):
                    os.mkdir(face_folder)
                
                new_filename = os.path.join(face_folder, file[0:-4]+'_'+str(i)+'.jpg')
                cv2.imwrite(new_filename, face)
            
    
if __name__== "__main__":
    parser = argparse.ArgumentParser(description='crop face from images')
    parser.add_argument('--path', default = 'folder path containing images',
                        help='path of the image folder')
    
    args = parser.parse_args()
    
    main(path = args.path)