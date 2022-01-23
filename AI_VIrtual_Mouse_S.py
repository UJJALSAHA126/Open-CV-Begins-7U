import pyautogui as pyauto
import os
import time
import cv2 as cv
import HandTrackingModeul_S as htm
import numpy as np

wScr , hScr = pyauto.size()
wScr = 1920
hScr = 1080

x3,y3 =0,0

cap =cv.VideoCapture(0)
cap.set(3,wScr)
cap.set(4,hScr)

pTime = 0

detector = htm.handDetector(1)

# print(wScr,hScr)
while True:
    #Find HandLandMarks
    success , img =cap.read()
    img = cv.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    # print(lmList)
    # Get the tip of the index and middle finger
    if (len(lmList)!=0) :
        x1 , y1 = lmList[8][1:]
        x2 , y2 = lmList[12][1:]
        # print((x1,y1),(x2,y2))
    # check which fingers are up
        fingers=[]
        fingers = detector.fingerUp()
        # print(fingers)            
    # Only Index Finger : Moving
        if(fingers[1]==1 and fingers[2]==0) :
            # Convert Coordinates
            x3 = np.interp(x1,(0,wScr),(0,wScr))
            y3 = np.interp(y1,(0,hScr),(0,hScr))
            # Smoothen Values --> Here I Don't Use This
            # Move Mouse
            currentPos = pyauto.mouseinfo.position()        # Found mouse current Pos
            pyauto.move(x3 - currentPos[0],  y3-currentPos[1])
            # pyauto._mouseMoveDrag(x3,y3)
            cv.circle(img,(x1,y1),15,(0,0,255),cv.FILLED)

    # Both Index and Middle Fingers are up : Clicking Mode
        if(fingers[1]==1 and fingers[2]==1) :
            # Find Distance Between Finges
            cv.circle(img,(x1,y1),15,(255,0,0),cv.FILLED)
            cv.circle(img,(x2,y2),15,(255,0,0),cv.FILLED)
            length,mouseinfo = detector.findDistance(8,12,img,False)
            # print(length,cx,cy)
            # Click Mouse if Distance Short
            if (length<60) :
                cv.circle(img,(mouseinfo[4],mouseinfo[5]),15,(255,0,255),cv.FILLED)
                pyauto.click()

    # Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    # Display
    cv.putText(img,str(int(fps)),(20,50),cv.FONT_HERSHEY_COMPLEX,3,(255,255,0),3)
    cv.imshow("Image",img)
    if(cv.waitKey(1)==ord('d')) :
        break

cap.release()
cv.destroyAllWindows()    