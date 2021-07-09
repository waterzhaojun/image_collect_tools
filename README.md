# image_collect_tools
This is a series of tools used for video recording, extract images and crop images

crop_object is a cropping tool by using mobilenet model to detect object and crop it.

extract_image: tools to extract images from video. You need to put your video in source folder. The output images will be saved in output folder.

sketch.py<br>
Convert a normal image to sketch image. Default path is a img.jpg file in same folder.

# 我打算建一个合并图像的py，注意fluorescent 的image如果要合并时，最好只取0.75的内容，否则边缘的亮度有变化。

# 目前我在dlc-macOS-CPU这个env来运用这个module