import numpy as np
import cv2

import time
# 你可以用这个file对各步骤对时间消耗进行测试

t = time.time()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(3,640)
cap.set(4,480)
while(True):
    t1 = time.time()
    ret, frame = cap.read() #这一步是最费时的，需要50-90ms
    print(time.time() - t1)
    if ret == True:
        
        cv2.imshow('frame',frame) #这一步小于1ms
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'): #这一步居然要大概15ms
            break
        
        # newt = time.time()
        # print(newt-t)
        # t = newt
    else:
        print('no %f' % (time.time() - t))
    
cap.release()
cv2.destroyAllWindows()
