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

# Get user supplied values
imagePath = "content.jpg" #sys.argv[1]
cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
    #flags = cv2.CV_HAAR_SCALE_IMAGE
)

for (x, y, w, h) in faces:
    #cv2.rectangle(image, (x-int(w*0.5), y-int(h*0.5)), (x+int(w*1.5), y+int(h*1.5)), (0, 255, 0), 2)
    x1 = x-int(w*0.5)
    x2 = x+int(w*1.5)
    y1 = y-int(h*0.6)
    y2 = y+int(h*1.4)
    crop_img = image[y1:y2, x1:x2]
    break

resize = ResizeWithAspectRatio(crop_img, height=1600)

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.imshow("window", resize)
cv2.waitKey(0)

#command = "python3 strotss.py scene_me.jpg RKlimt.jpg --weight 0.5 --output main_portrait.png --device {}".format('cuda:0')
#os.system(command)