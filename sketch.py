import cv2
import argparse
import os

def dodgeV2(image, mask):
    return cv2.divide(image, 255-mask, scale=256)



#img_canvas = cv2.imread("img_canvas.jpg")
#img_blend = cv2.multiply(img_blend, img_canvas, scale=1/256)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='record video')
    parser.add_argument('--path', default = 'img.jpg',
                        help='the path of the image')

    args = parser.parse_args()

    path = args.path
    filename = os.path.basename(path)
    dirname = os.path.dirname(path)
    outputfile = filename.split('.')[0]+'_sketch.'+filename.split('.')[1]
    outputpath = os.path.join(dirname, outputfile)
    print(filename, dirname, outputfile, outputpath)

    img_rgb = cv2.imread(path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_gray_inv = 255 - img_gray
    img_blur = cv2.GaussianBlur(img_gray_inv, ksize=(21, 21), sigmaX=0, sigmaY=0)
    img_blend = dodgeV2(img_gray, img_blur)

    cv2.imwrite(outputpath, img_blend)