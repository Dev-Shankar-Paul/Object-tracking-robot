#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 20:47:34 2020

@author: dsp
"""
# This program can be used to set the colour of the object to be 
# detected

import cv2
import numpy as np

def TestCam(source):
    cap = cv2.VideoCapture(source)
    check = cap.read()
    if(check[0] == False):
        print("Unable to access preferred camera!\n\nSwitching to "+
              "default camera!\n")
        return 0
    else:
        print("Using preferred camera!\n")
        return source
    
VideoCamera = 2    
cap = cv2.VideoCapture(TestCam(VideoCamera))

cv2.namedWindow('Trackbars')
cv2.createTrackbar("L-H", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("U-H", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("U-S", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("U-V", "Trackbars", 0, 255, lambda x:x)

while True:
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lh = cv2.getTrackbarPos("L-H", "Trackbars")
    ls = cv2.getTrackbarPos("L-S", "Trackbars")
    lv = cv2.getTrackbarPos("L-V", "Trackbars")
    uh = cv2.getTrackbarPos("U-H", "Trackbars")
    us = cv2.getTrackbarPos("U-S", "Trackbars")
    uv = cv2.getTrackbarPos("U-V", "Trackbars")
    
    mask = cv2.inRange(hsv, np.array([lh, ls, lv]), 
                       np.array([uh, us, uv]))
    cv2.imshow('mask', mask)
    
    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    
    frame = cv2.flip(frame, 1)
    cv2.imshow('Object detected', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()


