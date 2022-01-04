import os 
import cv2
import numpy as np
import sys

def crop_face(image):
    # Get user supplied values
    imagePath = image #"content.jpg" 
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

    if len(faces) >= 1:
        for (x, y, w, h) in faces:
            #cv2.rectangle(image, (x-int(w*0.5), y-int(h*0.5)), (x+int(w*1.5), y+int(h*1.5)), (0, 255, 0), 2)
            x1 = x-int(w*0.5)
            x2 = x+int(w*1.5)
            y1 = y-int(h*0.6)
            y2 = y+int(h*1.4)
            crop_img = image[y1:y2, x1:x2]
            break
    else:
        crop_img = image

    return crop_img
