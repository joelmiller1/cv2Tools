# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 08:18:23 2019
@author: Joel Miller
"""

import cv2

usps_cascade = cv2.CascadeClassifier('detect/uspsCascade.xml')
cap = cv2.VideoCapture('Videos/18_October_2019.mp4')

while True:
    success, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    usps = usps_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in usps:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
    
    cv2.imshow('Video',frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or not success:
        break

cap.release()
cv2.destroyAllWindows()

