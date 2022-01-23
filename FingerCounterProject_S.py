import cv2
import os
import time
import HandTrackingModeul_S as htm

wCam , hCam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath = "FingerImg"
myList = os.listdir(folderPath)

# print(myList)
overlayList = []
for imPath in myList :
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))

pTime = 0
detector = htm.handDetector()
tipIds = [4,8,12,16,20]

while True :
    succes , img = cap.read()
    img = cv2.flip(img,1)
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)

    
    

    if(len(lmList)!=0) :
        fingers = []
        #Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1] :
            fingers.append(1)
        else :
            fingers.append(0)
        #Four Fingers
        for id in range(1,5) :
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2] :
                fingers.append(1)
            else :
                fingers.append(0)
        # print(fingers) 
        totalFingers = fingers.count(1)
        print(totalFingers)
        h,w,c = overlayList[totalFingers-1].shape
        img[0:h,0:w]=overlayList[totalFingers-1]
        
        cv2.putText(img,f'{str(totalFingers)}',(50,h+30),cv2.FONT_HERSHEY_COMPLEX,1,(4, 0, 246),3)

          

    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS : {int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,1,(4, 0, 246),3)
    cv2.imshow("Image",img)

    if(cv2.waitKey(1) == ord('d')) :
             break
        # cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()