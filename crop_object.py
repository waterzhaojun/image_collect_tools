#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 23:51:07 2018

@author: Melody
"""

import tensorflow as tf
import cv2
import argparse
import os
import numpy as np
# import shutil

objid= 18 # person is 1, dog is 18

froze_model_path = '/Users/Melody/OneDrive/MLprojects/classification/models/ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb'
model_dir = os.path.dirname(froze_model_path)

ori_dir = '/Users/Melody/Documents/IMG/dog'
crop_dir = '/Users/Melody/Documents/IMG/dog_crop'
if not os.path.exists(crop_dir):
    os.mkdir(crop_dir)

folders = os.listdir(ori_dir)
folders = [x for x in folders if x[0] is not '.']

for f in folders:
    newpath = os.path.join(crop_dir, f)
    if not os.path.exists(newpath):
        os.mkdir(newpath)

imagepath = '/Users/Melody/Documents/IMG/dog/Great_Dane/n02109047_12899.jpg'
img = cv2.imread(imagepath)
img1 = np.expand_dims(img, axis=0)

def crop(image, box):
    __, height, width, __ = image.shape
    newbox = (box * [height, width, height, width]).astype(int)
    image_crop = image[0, newbox[0]:newbox[2], newbox[1]:newbox[3], :]
    return(image_crop)

graph = tf.Graph()

with graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(froze_model_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
        
num_detections_tensor = tf.squeeze(graph.get_tensor_by_name('num_detections:0'), 0)
num_detections_tensor = tf.cast(num_detections_tensor, tf.int32)

detected_boxes_tensor = tf.squeeze(graph.get_tensor_by_name('detection_boxes:0'), 0)
detected_boxes_tensor = detected_boxes_tensor[:num_detections_tensor]

detected_scores_tensor = tf.squeeze(graph.get_tensor_by_name('detection_scores:0'), 0)
detected_scores_tensor = detected_scores_tensor[:num_detections_tensor]

detected_labels_tensor = tf.squeeze(graph.get_tensor_by_name('detection_classes:0'), 0)
detected_labels_tensor = tf.cast(detected_labels_tensor, tf.int64)
detected_labels_tensor = detected_labels_tensor[:num_detections_tensor]

image_tensor = graph.get_tensor_by_name('image_tensor:0')


with tf.Session(graph = graph) as sess:
    for f in folders:
        files = os.listdir(os.path.join(ori_dir, f))
        files = [x for x in files if x[-3:] in ['jpg', 'JPG']]
        for fl in files:
            imagepath = os.path.join(ori_dir, f, fl)
            img = np.expand_dims(cv2.imread(imagepath), axis = 0)

            y = sess.run((detected_labels_tensor, detected_boxes_tensor, detected_scores_tensor), 
                          feed_dict={image_tensor:img})
            
            idx = np.where(y[0] == objid)[0]
            
            if len(idx)>0:
                for i in range(len(idx)):
                    box = y[1][idx[i]]
                    img_crop = crop(img, box)
                    cv2.imwrite(os.path.join(crop_dir, f, fl[0:-4]+'_'+str(i)+'.jpg'), img_crop)
        

        


!tensorboard --logdir=$model_dir


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