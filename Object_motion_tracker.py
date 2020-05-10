#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:15:32 2020

@author: dsp
"""
import cv2
import numpy as np

lower_red = np.array([0, 0, 0])
upper_red = np.array([113, 113, 113])

points = []

cap = cv2.VideoCapture(0)
"""
ret, frame = cap.read()
height, width = frame.shape[: 2]
frame_count = 0
"""
backsub = cv2.createBackgroundSubtractorKNN()

while True:
    ret, frame = cap.read()
    hsv_image = cv2.GaussianBlur(frame, (3,3), 7)
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    mask = cv2.inRange(hsv_image, lower_red, upper_red)
    
    #res = cv2.bitwise_and(frame, frame, mask = mask)
    edges = cv2.Canny(mask, 0, 150)
    contours, hierarchy = cv2.findContours(edges, 
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    for c in contours:
        M = cv2.moments(c)
        if(M["m00"] != 0):
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
    
    #fgmask = backsub.apply(res)
    
    cv2.drawContours(mask, contours, -1, (0, 255, 0), 3)
    cv2.circle(frame, (cx, cy), 50, (0, 255, 0), 3)
    
    cv2.imshow('Original frame', hsv_image)
    cv2.imshow('mask', mask)
    #cv2.imshow('final', res)
    #cv2.imshow('Bkg_Subtracted', fgmask)  
    #cv2.imshow('edges', edges)
    #cv2.imshow('Contour', frame)
    
    cv2.imshow('Object detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

