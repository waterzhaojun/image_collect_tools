import cv2

is_working = True
dev_port = 0
working_ports = []
available_ports = []

for i in range(10):
    camera = cv2.VideoCapture(i)
    if not camera.isOpened():
        is_working = False
        print('Port %s is not working.' % i)
    else:
        is_reading, img = camera.read()
        w = camera.get(3)
        h = camera.get(4)
        if is_reading:
            print('Port %s is working and reads images (%s x %s)' % (i, w, h))
        else:
            print('Port %s for camera (%s x %s) is present but does not reads' % (i, w, h))