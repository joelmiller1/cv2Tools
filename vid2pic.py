# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 21:26:07 2019

@author: Me
"""

import cv2,glob,os

#TODO: add argparse for command line usage

def bgList(vidPath,picPath):
    vidcap = cv2.VideoCapture(vidPath)
    imgList = []
    currentDir = os.getcwd()
    os.chdir(picPath)
    for file in glob.glob('*.jpg'):
        imgList.append(file)
    os.chdir(currentDir)
    count = len(imgList) + 1
    
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite(picPath+"/img"+str(count)+".jpg", image)     # save frame as JPG file
        return hasFrames,image
    
    sec = 0
    frameRate = 2 #//it will capture image in each 0.5 second
    success,image  = getFrame(sec)
    
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success,image = getFrame(sec)
        
        if success:
            cv2.imshow("video",image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        
    vidcap.release()
    cv2.destroyAllWindows()
    print("Done.")





