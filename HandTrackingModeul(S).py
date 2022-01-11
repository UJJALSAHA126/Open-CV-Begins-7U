import cv2
import mediapipe as mp
import time


class handDetector() :
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
          

        self.mpHands = mp.solutions.mediapipe.python.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,1,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
        
        self.circlecolor=self.mpDraw.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2) # Changing the connecion Colors
        self.ccolor=self.mpDraw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)                 
                   


    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS,
                    self.circlecolor,self.ccolor)
        return img

    def findPosition(self,img,handno=0,draw=True):  

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handno]
            for id , lm in enumerate(myHand.landmark) :
                        # print(id,str(lm))
                h,w,c = img.shape
                cx , cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,255,255),cv2.FILLED)
        return lmList

def main() :
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True :
        success , img = cap.read()
        img = detector.findHands(img)
        # lmList = detector.findPosition(img)
        # if len(lmList)!=0 :
            # print(lmList[4])
            # pass
        cTime = time.time()
        fps = 1/(cTime-pTime) 
        pTime = cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,255,0),3)
        cv2.imshow("Image",img)
        if cv2.waitKey(1) == ord('d') :
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ =="__main__" :
    main()