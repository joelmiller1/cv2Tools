# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 21:26:07 2019

@author: Me
"""

import cv2,glob,os,argparse

def main():
    parser = argparse.ArgumentParser(description='convert videos to pictures')
    parser.add_argument('-v', '--vidPath', required=True,
                        help='path to the video')
    parser.add_argument('-o', '--picPath', required=True,
                        help='path to the where you want the pictures')
    parser.add_argument('-r', type=int,
                        help='how often to capture pictures')
    
    # Video Path
    args = vars(parser.parse_args())
    vidPath = args['vidPath']
    
    # Picture path -- if no folder, create one
    picPath = args['picPath']
    if os.path.isdir(picPath) == False:
        os.mkdir(picPath)
    
    # Default frame rate is 1 image per second
    frameRate = args['r']
    if frameRate == None:
        frameRate = 1
        
    bgList(vidPath,picPath,frameRate)

def bgList(vidPath,picPath,frameRate):
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

if __name__ == '__main__':
    main()


