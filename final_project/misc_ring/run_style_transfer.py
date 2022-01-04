import os 
import cv2
import numpy as np
import sys

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def run_strotss(scene_or_face, path_to_content, path_to_style):
	if scene_or_face == 'face':
		command = "python3 strotss.py {} {} --weight 0.5 --output main_portrait.png --device {}".format(path_to_content, path_to_style, 'cuda:0')
	if scene_or_face == 'scene':
		command = "python3 strotss.py {} {} --weight 0.5 --output main_scene.png --device {}".format(path_to_content, path_to_style,'cuda:0')
	os.system(command)

resize = ResizeWithAspectRatio(crop_img, height=1600)

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.imshow("window", resize)
cv2.waitKey(0)