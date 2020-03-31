import time,cv2,collections,math
from areaSelect import areaSelector

min_threshold = 20
min_area = 700
cap = cv2.VideoCapture('../vids/cctv2.mp4')
timeout = time.time() + 5
timeBuffer = collections.deque(maxlen=30)
pixelBuffer = collections.deque(maxlen=30)

cap.set(cv2.CAP_PROP_POS_MSEC, 5000)
success, refFrame = cap.read()
mask = areaSelector(refFrame)

def ref_frame():
    success, refFrame = cap.read()
    refFrame = refFrame[mask]
    if success:
        refGray = cv2.cvtColor(refFrame, cv2.COLOR_BGR2GRAY)
        refGray = cv2.GaussianBlur(refGray, (21, 21), 0)
        return refGray, refFrame
refGray, refFrame = ref_frame()

def calcMPH(frame,fps,pixelDelta):
    pixelWidth = frame.shape[1]
    meters2PixelWidth = 20/pixelWidth  # hard coded, 20 meters per total pixel width
    metersPerSecond = (pixelDelta/fps)*meters2PixelWidth
    mps2mph = metersPerSecond * 2.23694
    return mps2mph

def detectMotion():
    timeBuffer.append(time.time())
    success, frame = cap.read()
    frame = frame[mask]
    if success:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        frameDelta = cv2.absdiff(refGray, gray)
        thresh = cv2.threshold(frameDelta, min_threshold, 255, cv2.THRESH_BINARY)[1]
        thresh2 = cv2.dilate(thresh, None, iterations=2)
        contours = cv2.findContours(thresh2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = contours[0]
        fps = 0
        pixelDelta = 0
        for c in cnts:
            if cv2.contourArea(c) > min_area:
                (x, y, w, h) = cv2.boundingRect(c)
                pixelBuffer.append(x+w)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                if len(timeBuffer) >= 2:
                    tEnd = timeBuffer.pop()
                    tStart = timeBuffer.pop()
                    fps = 2/(tEnd-tStart)
                    if len(pixelBuffer) >= 2:
                        pEnd = pixelBuffer.pop()
                        pStart = pixelBuffer.pop()
                        pixelDelta = abs(pEnd - pStart)
                        mph = round(calcMPH(frame,fps,pixelDelta),1)
                        cv2.putText(frame,str(mph)+' mph',(x,y),cv2.FONT_HERSHEY_DUPLEX,0.4,(255,255,0),1)
        return frame, fps, pixelDelta
    return 0, 0, 0

while True:
    # refresh first frame compare every 10 seconds
    if time.time() > timeout:
        timeout = time.time() + 2
        refGray, refFrame = ref_frame()

    frame,fps,pixelDelta = detectMotion()

    cv2.imshow("Video",frame)

    key = cv2.waitKey(90) & 0xFF
    if key == ord("q"):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
