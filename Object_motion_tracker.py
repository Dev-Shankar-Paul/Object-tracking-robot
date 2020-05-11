#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:15:32 2020

@author: dsp
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L-H", "Trackbars", 0, 179, lambda x:x)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("U-H", "Trackbars", 0, 179, lambda x:x)
cv2.createTrackbar("U-S", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("U-V", "Trackbars", 0, 255, lambda x:x)
    
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

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
    
    final = cv2.bitwise_and(frame, frame, mask = mask)
    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Final', final)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
