import cv2
import os
import numpy as np
import utils

config = utils.load_json(os.path.join('lib', 'config.json'))

# Choose video and output folder
videolist = os.listdir(config['sourceFolder'])
tmp = utils.select('Choose the video you want to extract: ', videolist, defaultChoose=0)
videopath = os.path.join(config['sourceFolder'], tmp)
outputFolder = os.path.join(config['outputFolder'], os.path.basename(videopath)[:-4])
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

# Set how many frames you want
tmp = input('how many images you want (Press ENTER for default 10): ')
if tmp == '':
    imageNum = 10
else:
    imageNum = int(tmp)

# Choose the period you want
tmp = input('Set the period you want to extract (Unit is min. format is like 2-10): ')
if tmp == '':
    period = None
else:
    period = np.array(tmp.split('-')).astype(int)

# Choose the way to extract image
extract_method_list = ['equal', 'random']
extract_method = utils.select('Extract method: ', extract_method_list, defaultChoose=0)


# load Video
cap = cv2.VideoCapture(videopath)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)


if period is not None:
    period = np.multiply(period, fps*60).astype(int)
    period = np.array([np.maximum(0, period[0]), np.minimum(length, period[1])])
else:
    period = [0, length]

if extract_method == 'equal':
    idxes = np.linspace(period[0], period[1], imageNum)
elif extract_method == 'random':
    idxes = np.random.choice(np.arange(period[0], period[1]), imageNum)
else:
    raise ValueError('Please confirm your extract method')

print('Video length: %f min. FPS = %f' % (length/fps/60, fps))
print('Extract %d/%d images from %.2f to %.2f min.' % (imageNum, length, period[0]/fps/60, period[1]/fps/60))

# Start to extract images =================================================
for i in idxes:
    msid = int(i/fps*1000)
    print('%s done' % msid)

    # cap.set(1, i) # 1 means CV_CAP_PROP_POS_FRAMES, check the list at 
    # https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-set
    cap.set(0, msid)
    ret, frame = cap.read()
    

    if ret:
        filename = os.path.join(outputFolder, str(msid)+'.jpg')
        cv2.imwrite(filename, frame)

cap.release()
cv2.destroyAllWindows()