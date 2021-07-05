#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 22:55:29 2018

@author: Melody

The path should contain some subfolders, each subfolder is a class with class 
name as subfolder name.

The output will build an images folder contain all images, and a label.csv containing 
the label information.
"""

import os
import pandas as pd
import argparse
import shutil
import numpy as np
import math
import tensorflow as tf
import cv2

def create_train_test_idx_from_range_num(num, ratio = 0.8):
    
    trainidx = np.random.choice(num, size = int(math.floor(num*ratio)), replace = False)
    textidx = [x for x in list(range(num)) if x not in trainidx]
    
    return(trainidx, textidx)
    
def create_labelmap(path, output = True):
    folders = os.listdir(path)
    folders = [x for x in folders if os.path.isdir(os.path.join(path,x))]
    
    labelmap = pd.DataFrame(columns = ['classname', 'classid'])
    idx = 0
    for folder in folders:
        labelmap.loc[idx] = [folder, idx]
        idx =idx + 1
        
    labelmap.to_csv(os.path.join(path, 'labelmap.csv'), index = False)
    
    if output:
        return(labelmap)

def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def main(path, ratio, remove_tmp_folder, resize, size):
    
    tmpfolder = path+'_tmpoutput'
    if not os.path.exists(tmpfolder):
        os.mkdir(tmpfolder)
        
    labelfile = pd.DataFrame(columns = ['file', 'label'])
    
    labelmap = create_labelmap(path)
    
    idx = 0
    
    folders = os.listdir(path)
    folders = [x for x in folders if os.path.isdir(os.path.join(path,x))]
    
    
    for folder in folders:
        
        files = os.listdir(os.path.join(path, folder))
        files = [x for x in files if x[-3:] in ['jpg', 'JPG']]
        
        for file in files:
            
            shutil.copyfile(os.path.join(path, folder, file), 
                            os.path.join(tmpfolder, folder+'_'+file))
            classid = labelmap.loc[labelmap.loc[:,'classname'] == folder, 'classid'].values[0]
            
            labelfile.loc[idx] = [os.path.join(tmpfolder, folder+'_'+file), classid]

            idx = idx + 1
          
    labelfile.to_csv(os.path.join(tmpfolder, 'label.csv'), index = False)
    
    # ======================
    
    
    tffile = dict()
    (tffile['train'], tffile['test']) = create_train_test_idx_from_range_num(len(labelfile), ratio)
    
    for i in ['train', 'test']:
        tffile_name = os.path.join(path, i+'.tfrecord')
        
        writer = tf.python_io.TFRecordWriter(tffile_name)
        
        for j in tffile[i]:
            image = cv2.imread(labelfile.loc[j,'file'])
            if resize:
                image = cv2.resize(image, size)
                
            label = labelfile.loc[j,'label']
            height, width, depth = image.shape
            
            feature = {'label': _int64_feature(label),
                       'image': _bytes_feature(tf.compat.as_bytes(image.tostring()))
                       #'height': _int64_feature(height),
                       #'width': _int64_feature(width),
                       #'depth': _int64_feature(depth)
                       }
            
            example = tf.train.Example(features=tf.train.Features(feature=feature))
            
            writer.write(example.SerializeToString())
            
        writer.close()
        
    if remove_tmp_folder:
        shutil.rmtree(tmpfolder)
        

        
        
            
if __name__== "__main__":
    parser = argparse.ArgumentParser(description='from folder to create images folder and label.csv')
    parser.add_argument('--path', required = True,
                        help='path of the folder containing several subfolders')
    parser.add_argument('--ratio', default = 0.8,
                         type = float,
                         help = 'the ratio of train sample')
    parser.add_argument('--remove_tmp_folder', default = True,
                        type = bool, help = 'whether remove the tmp folder after the process')
    parser.add_argument('--resize', default = True,
                        type = bool, help = 'whether resize the images')
    parser.add_argument('--size', default = (299, 299),
                        type = int, help = 'if resize the image, what is the new size')
    args = parser.parse_args()
    
    main(path = args.path, ratio = args.ratio, 
         remove_tmp_folder = args.remove_tmp_folder, resize = args.resize,
         size = args.size)