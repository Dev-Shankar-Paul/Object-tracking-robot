#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:15:32 2020

@author: dsp
"""
import cv2
import numpy as np
from statistics import mode
import math

def distance(a, b):
    dist = math.sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)
    return dist

cap = cv2.VideoCapture(0)
distances = []

# Create the trackbars to manually set the hue, saturation 
# and value of the image to be tracked 
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L-H", "Trackbars", 0, 179, lambda x:x)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("U-H", "Trackbars", 0, 179, lambda x:x)
cv2.createTrackbar("U-S", "Trackbars", 0, 255, lambda x:x)
cv2.createTrackbar("U-V", "Trackbars", 0, 255, lambda x:x)

x_max = 640
y_max = 480

# Setting the values of the corner-points (clockwise from top-left)
corners = {
    'c1' : (0, 0),
    'c2' : (x_max, 0),
    'c3' : (x_max, y_max),
    'c4' : (0, y_max)}


while True:
    
    ret, frame = cap.read()
    #frame = cv2.GaussianBlur(frame, (5,5), 3)
    # drawing the corner points of the frame
    for i in corners:
        cv2.circle(frame, corners[i], 5, (0, 0, 255), -1)
        
    # convert the image to HSV to allow InRange to work on it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # prep the taskbars and get the values from them by manual
    # adjustment
    lh = cv2.getTrackbarPos("L-H", "Trackbars")
    ls = cv2.getTrackbarPos("L-S", "Trackbars")
    lv = cv2.getTrackbarPos("L-V", "Trackbars")
    uh = cv2.getTrackbarPos("U-H", "Trackbars")
    us = cv2.getTrackbarPos("U-S", "Trackbars")
    uv = cv2.getTrackbarPos("U-V", "Trackbars")
    
    # Thresholding the image to obtain the mask
    mask = cv2.inRange(hsv, np.array([lh, ls, lv]), 
                       np.array([uh, us, uv]))
    #cv2.imshow('Mask', mask)
    
    # performing bitwise AND operation to layer mask over frame
    #final = cv2.bitwise_and(frame, frame, mask = mask)
    #cv2.imshow('Final', final)
    
    # utilise the mask to get contours and plot them on frame
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    #cv2.imshow('Contours', frame)
     
    # If contours is not an empty list, loop through it to find
    # the center of the contour using moments 
    list_cx = []
    list_cy = []
    if(contours != []):
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
            
            M = cv2.moments(c)
            if(M["m00"] != 0):
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = cx, cy
    else:
        cx, cy = int(x_max/2), int(y_max/2)
    
    # drawing the line which is to be used to find angle
    #cv2.line(frame, (int(x_max/2), 0), (int(x_max/2), int(y_max)),
    #         (0, 255, 0), 3)
    #cv2.line(frame, (0, int(y_max/2)+100), (x_max,int(y_max/2)+100) ,
    #         (0, 255, 0), 3)
    #cv2.line(frame, (0, int(y_max/2)-100), (x_max, int(y_max/2)-100),
    #         (0, 255, 0), 3)
    # Draw a circle showing the part that was detected. The list 
    # thing is used to stabilise the readings a little bit. 
    # Ask Tony Bhaiya.
    list_cx.append(cx)
    list_cy.append(cy)
    point = (mode(list_cx),mode(list_cy))
    
    #cv2.circle(frame, point, 5, (0, 255, 0), 3)
    
    # check if the object is in the left half of the window or the 
    # right half of the window
    left_distance = distance(point, corners['c1'])+distance(point, corners['c4'])
    right_distance = distance(point, corners['c2'])+distance(point, corners['c3'])
    
    if(left_distance < right_distance):
        cv2.rectangle(frame, (0,0), (int(x_max/2), int(y_max)),
                      (0, 0, 255), 3)
    elif(right_distance < left_distance):
        cv2.rectangle(frame, (int(x_max/2), 0), 
                      (x_max, y_max), (0, 0, 255), 3)
    
    # Get the angle with some fancy math
    perpendicular = math.sqrt((point[0]-int(x_max/2))**2)
    base = point[1]
    if(base != 0):
        angle = math.atan(perpendicular/base)
        angle = angle * 180/3.14
    else:
        print('Infinity')
    print(int(angle/10)*10)
    
    # Flipping the frame to get mirror like image
    frame = cv2.flip(frame, 1)
    cv2.imshow('Object detected', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
