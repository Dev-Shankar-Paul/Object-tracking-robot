#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:15:32 2020

@author: dsp
"""
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('My laptop camera', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

