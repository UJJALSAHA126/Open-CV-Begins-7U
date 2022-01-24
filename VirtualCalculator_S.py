from random import randint
from re import L
from tkinter import Checkbutton
from turtle import width
import cv2 as cv
import HandTrackingModeul_S as htm
import time

cap = cv.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)

detector = htm.handDetector()

class Button :
    def __init__(self,pos,width,height,value) :
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self,img) :
        cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(0,255,0),cv.FILLED)
        cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
        cv.putText(img,str(self.value),(self.pos[0]+23,self.pos[1]+68),cv.FONT_HERSHEY_COMPLEX,2,(0,0,0),2)

    def clickButton(self,x,y,cx,cy) :
        if self.pos[0] < x <self.pos[0] + self.width and self.pos[1] < y < self.pos[1] +self.height:
            cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(0,255,0),cv.FILLED)
            cv.rectangle(img,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
            cv.putText(img,str(self.value),(self.pos[0]+23,self.pos[1]+68),cv.FONT_HERSHEY_COMPLEX,3,(0,0,0),3)
            cv.circle(img,(cx,cy),5,(255,0,0),15)
            return True 
        else : return False    

# Creating Buttons

buttonListValue = [['7','8','9','*'],
                    ['4','5','6','/'],
                    ['1','2','3','+'],
                    ['C','0','=','-']]

buttonLst = []
for x in range(4) :
    for y in range(4) :
        xpos = x*100 + 700
        ypos = y*100 + 150
        buttonLst.append(Button((xpos,ypos),100,100,buttonListValue[y][x]))

equation = ''
delayCounter=0

while True :
    success , img = cap.read()
    img= cv.flip(img,1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)

    cv.rectangle(img,(700,70),(700+400,70+100),(250,255,255),cv.FILLED)
    cv.rectangle(img,(700,70),(700+400,70+100),(50,50,50),3)

    for button in buttonLst :
        button.draw(img)

    

    if len(lmList)!=0 :
        length,mouseinfo = detector.findDistance(8,12,img,False)
        x1 , y1 = lmList[8][1:]
        x2 , y2 = lmList[12][1:]
        cv.circle(img,(x1,y1),5,(0,0,255),15)
        cv.circle(img,(x2,y2),5,(0,0,255),15)
        
        
        # Click Mouse if Distance Short
        if (length<60) :
            cx , cy = (x1+x2)//2 , (y1+y2)//2
            # cv.circle(img,(x2-x1)//2,(y2-y1)//2,5,(255,0,0),15)
            
            for i, button in enumerate(buttonLst) :
                if button.clickButton(x1,y1,cx,cy) and delayCounter==0 :
                    myValue = buttonListValue[int(i%4)][int(i/4)]
                    if myValue == "=" :
                        equation = str(eval(equation))
                    elif myValue == "C" :
                        equation = ''
                    else :
                        equation += myValue    
                    delayCounter = 1

        if delayCounter != 0 :
            delayCounter += 1
            if delayCounter >10 :
                delayCounter = 0

    cv.putText(img,equation,(710,130),cv.FONT_HERSHEY_COMPLEX,2,(0,0,0),2)

    cv.imshow("Screen",img)
    # if(cv.waitKey(1)==ord('c')) :
    #     equation = ''
    if(cv.waitKey(1)==ord('d')) :
        break

cap.release()
cv.destroyAllWindows() 