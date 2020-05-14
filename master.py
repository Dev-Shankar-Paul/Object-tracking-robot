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
angleP = 90

def left(a):
    return (int(90-a))

def right(a):
    return (int(90+a))

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

blue_lower = np.array([36, 111, 255])
blue_upper = np.array([153, 255, 255])

# Preferred camera
VideoCamera = 2
cap = cv2.VideoCapture(TestCam(VideoCamera))

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
            area = cv2.contourArea(c)
            
            if(area > 4150):
                print("OBJECT DETECTED!!")
                point, radius = cv2.minEnclosingCircle(c)
                x, y = int(point[0]), int(point[1])
                cv2.circle(frame, (x, y), int(radius),
                           (0, 255, 0), 3)
                center = (x, y)
                
            else:
                center = (int(x_max/2), int(y_max/2))
    
    else:
        print("NO OBJECT DETECTED!")
        center = (int(x_max/2), int(y_max/2))

    perpendicular = math.sqrt((center[0]-int(x_max/2))**2)
    base = center[1]
    
    if(base != 0):
        angle = math.atan(perpendicular/base)
        angle = angle * 180/3.14
        
        if(center[0] > x_threshold):
            value = left(angle)
        elif(center[0] < x_threshold):
            value = right(angle)
        else:
            value = 90
            
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
    
    
    
