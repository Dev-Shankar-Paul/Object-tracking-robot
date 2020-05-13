#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:25:31 2020

@author: dsp
"""
import cv2
import numpy as np
import math
import serial

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.flushInput()
value = 0

def left(a):
    return (int(90-a))

def right(a):
    return (int(90+a))

blue_lower = np.array([36, 111, 255])
blue_upper = np.array([153, 255, 255])

cap = cv2.VideoCapture(0)

x_max = 640
y_max = 480
x_threshold = x_max/2

while True:
    ret, frame = cap.read()
    blurred = cv2.GaussianBlur(frame, (5,5), 3)
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    
    if(contours != []):
        for c in contours:
            M = cv2.moments(c)
            if(M["m00"] != 0):
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = cx, cy
    else:
        cx, cy = int(x_max/2), int(y_max/2)
                
    center = (cx, cy)
    cv2.circle(frame, center, 5, (0, 255, 0), 3)

    perpendicular = math.sqrt((center[0]-int(x_max/2))**2)
    base = center[1]
    if(base != 0):
        angle = math.atan(perpendicular/base)
        angle = angle * 180/3.14
        
        # low pass filter
        angleP = angle
        angle = 0.94 * angleP + 0.06 * angle
    else:
        angle = 90
    if(cx > x_threshold):
        value = left(angle)
    elif(cx < x_threshold):
        value = right(angle)
    else:
        value = 90
        
    ser.write(b' ' + str(value).encode('ascii') + b'\n')
    
    frame = cv2.flip(frame, 1)
    cv2.imshow('Object detected', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    
ser.close()
cap.release()
cv2.destroyAllWindows()
    
    
    
