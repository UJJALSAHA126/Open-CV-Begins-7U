import os
import cv2 as cv
import numpy as np
import HandTrackingModeul_S as htm
import random

drawcolor = (0,255,0)
folder = "paintpic"
folderlist = os.listdir(folder)
# print(folderlist)
overlayList =[]
for impath in folderlist :
    image = cv.imread(f'{folder}/{impath}')
    overlayList.append(image)
# print(len(overlayList))

cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,780)

head=overlayList[0] 
detector = htm.handDetector()

imCanvas = np.zeros((720,1280,3),np.uint8)

while True :
    #Import LandMarks
    success , img = cap.read()
    img = cv.flip(img,1)
    
    
    #Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    
    imgGray = cv.cvtColor(imCanvas,cv.COLOR_BGR2GRAY)
    _,imgInv = cv.threshold(imgGray,0,255,cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv,cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img,imgInv)
    img = cv.bitwise_or(img,imCanvas)
    
    if(len(lmList)!=0) :
        # print(lmList)
        xp , yp =0,0
        #tip of index and middle finger
        x1 , y1 = lmList[8][1:]
        x2 , y2 = lmList[12][1:]

        #Check Which Finger is up
        finger = detector.fingerUp()
        # print(finger)
        #Selection Mode
        if finger[1] and finger[2] :
            print("Selection")
            if y1<125 :
                if 0<x1<200:
                    img_name = f'PainterPic{random.randint(1,10)}.jpg'
                    img_name1 = f'PainterPic{random.randint(100,200)}.jpg'

                    cv.imwrite(f'{folder}/{img_name}',imCanvas)
                    cv.imwrite(f'{folder}/{img_name1}',img)
                    # cv.imwrite(img_name,img)
                    print("Saved")
                    break
                elif 250<x1<450 :
                    head = overlayList[0]
                    drawcolor=(0,255,0)
                elif 550<x1<750 :
                    head = overlayList[1]
                    drawcolor=(255,0,0)
                elif 800<x1<950 :
                    head = overlayList[2]
                    drawcolor=(0,0,255)
                else :
                    head = overlayList[3]
                    drawcolor=(0,0,0)
            cv.rectangle(img,(x1,y1),(x2,y2),drawcolor,cv.FILLED)
        

        #Paint Mode / Draw Mode
        if finger[1] and finger[2]==False:
            cv.circle(img,(x1,y1),5,drawcolor,15)
            print("Draw")    
            if xp==0 and yp==0 :
                xp,yp = x1,y1
            if drawcolor == (0,0,0) :    
                cv.line(img,(xp,yp),(x1,y1),drawcolor,30)
                cv.line(imCanvas,(xp,yp),(x1,y1),drawcolor,30)
            else :    
                cv.line(img,(xp,yp),(x1,y1),drawcolor,15)
                cv.line(imCanvas,(xp,yp),(x1,y1),drawcolor,15)
            xp ,yp = x1,y1
                
    

    

    img[0:125,0:1280]=head
    cv.imshow("CAP",img)
    cv.imshow("Canvas",imCanvas)
    if(cv.waitKey(1)==ord('d')) :
        break

cap.release()
cv.destroyAllWindows()