# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:28:17 2020

@author: Joel Miller
"""

import cv2,os
from datetime import datetime, timedelta

minThreshold = 45
minArea = 1100

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
if not os.path.isdir('motionVids'):
    os.mkdir('motionVids')
success, frame = cap.read()
refFrame = frame.copy()
timestamp = datetime.now() + timedelta(seconds=7)
motionTimeout = datetime.now()
motionFlag = False
videoWriteEnable = False
startRecord = True

while True:
    success, frame = cap.read()
    if not success: break
    if datetime.now() >  timestamp:
        timestamp = datetime.now() + timedelta(seconds=4)
        refFrame = frame.copy()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)        
    grayRef = cv2.cvtColor(refFrame, cv2.COLOR_BGR2GRAY)
    grayBlur = cv2.GaussianBlur(gray, (21, 21), 0)
    grayRefBlur = cv2.GaussianBlur(grayRef, (21, 21), 0)
    frameDelta = cv2.absdiff(grayBlur, grayRefBlur)
    thresh = cv2.threshold(frameDelta, minThreshold, 255, cv2.THRESH_BINARY)[1]
    thresh2 = cv2.dilate(thresh, None, iterations=2)
    contours = cv2.findContours(thresh2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = contours[0]
    for c in cnts:
        if cv2.contourArea(c) > minArea:
            if videoWriteEnable:
                motionFlag = True
                if startRecord:
                    print("motion record started")
                    fileName = datetime.now().strftime("motionVids/%y_%m_%d_%H%M%S") + ".mp4"
                    vw = cv2.VideoWriter(fileName,fourcc,24,(640,480))
                    startRecord = False
            motionTimeout = datetime.now() + timedelta(seconds=3)
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),1)
    
    if motionFlag:
        vw.write(frame)
    try:
        if datetime.now() > motionTimeout and vw.isOpened():
            motionFlag = False
            print("motion record ended")
            vw.release()
            startRecord = True
    except:
        pass
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        try:
            if vw.isOpened():
                vw.release()
            break
        except:
            break
    if key == ord("s"):
        videoWriteEnable = True
        print("Video write enabled")
        
    cv2.imshow('Video',frame)
    

cap.release()
cv2.destroyAllWindows()
