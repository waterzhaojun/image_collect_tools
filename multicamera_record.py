from threading import Thread
import cv2
import time
import numpy as np
import os
import json
import math
import datetime
import shutil

# 这个版本是我目前最新的版本，是用multi thread来执行多camera的记录。

def load_config():
    configpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib', 'config.json')
    with open(configpath, 'r') as f:
        config = json.load(f)
    return(config)


class Recorder:
    def __init__(self, name, port, savepath, config, monitorframe, rid, cid):
        self.name = name
        self.cam = cv2.VideoCapture(port)

        # 设置好采集的尺寸，否则画面会变形
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, config['output_video_width'])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, config['output_video_height'])
        self.videosize = (config['output_video_width'], config['output_video_height']) # 导出video的size
        self.monitorsize = (config['monitor_video_width'], config['monitor_video_height']) # 输出到moniter的size
        self.writer = cv2.VideoWriter(savepath, 0, 
            fourcc = cv2.VideoWriter_fourcc(*[x for x in config['fourcc']]), 
            fps = config['video_write_rate'], 
            frameSize = self.videosize)
        self.target_r_pos = [rid * self.monitorsize[1], (rid+1) * self.monitorsize[1]]
        self.target_c_pos = [cid * self.monitorsize[0], (cid+1) * self.monitorsize[0]]
        self.monitorframe = monitorframe
        self.record_flag = False
        self.end_flag = False
        self.tic = 0
        self.counter = 0
        self.thread = None

    def start(self):    
        self.thread = Thread(target=self.run, args=())
        self.thread.start()

    def run(self):
        while True: 
            ret, frame = self.cam.read()
            if ret:
                videoframe = cv2.resize(frame, self.videosize) # 即使你对writer已经设了大小，你也得先resize一下，否则视频不能放
                self.monitorframe[self.target_r_pos[0]:self.target_r_pos[1], self.target_c_pos[0]:self.target_c_pos[1], :] = cv2.resize(frame, self.monitorsize)
                if self.record_flag and ((self.counter / config['video_write_rate']) < (time.time()-self.tic)):
                    self.writer.write(videoframe)
                    self.counter += 1
                    print('%s: %f' % (self.name, round(time.time() - self.tic, 1)))
            
            if self.end_flag:
                break

        self.cam.release()
        return(None) #如果return，这里thread就会自动结束，我觉得可能不加也没关系。
            
    
    def stop(self):
        self.end_flag = True

# Load config
config = load_config()
ports = config['port_list']
cols = config['monitor_col_num']
rows = int(math.ceil(len(ports)/2))
monitorframe = np.zeros((config['monitor_video_height'] * rows, config['monitor_video_width'] * cols, 3), np.uint8)

# Set file name
thedate = datetime.datetime.now().date().strftime('%Y-%m-%d')
thetime = datetime.datetime.now().time().strftime('%H-%M-%S')
savefolder = os.path.join(config['outputFolder'], thedate + ' ' + thetime)

if not os.path.exists(savefolder):
    os.mkdir(savefolder)

# Add cameras
cams = []
for i in range(len(ports)):
    cams.append(Recorder('cam_port' + str(ports[i]), ports[i], os.path.join(savefolder, 'cam_port' + str(ports[i]) + '.mov'), config, monitorframe, math.floor(i/cols), i%cols))

# Start each cameras
for c in cams:
    c.start()

while True:
    cv2.imshow('monitor', monitorframe)
    keyinput = cv2.waitKey(1) & 0xFF
    if keyinput == ord('s'):
        print('start to record')
        for c in cams:
            c.record_flag = True
            c.tic = time.time()
    elif keyinput == ord('q'):
        print('Start to close cameras.')
        for c in cams:
            c.stop()
        
        for i in range(3):
            print('The record will finish in %d sec.' % i)
            time.sleep(1)

        cv2.destroyAllWindows()
        if len(os.listdir(savefolder)) == 0:
            shutil.rmtree(savefolder)
        break

# t1.join()
# t2.join()