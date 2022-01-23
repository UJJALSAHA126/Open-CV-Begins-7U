import cv2 
import time
import mediapipe as mp

# cap = cv2.VideoCapture("Videos/vid2.mp4")

class FaceDetector() :
    def __init__(self,minDetectionCon=0.5):

        self.minDetectionCon = minDetectionCon
        self.myFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.myFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self,img,draw=True) :
        imRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imRGB)

        bboxs = []
        if self.results.detections :
            for id , detection in enumerate(self.results.detections) :
                
                bboxC = detection.location_data.relative_bounding_box
                ih ,iw, ic = img.shape
                bbox= int(bboxC.xmin * iw) , int(bboxC.ymin * ih) ,\
                    int(bboxC.width * iw) , int(bboxC.height * ih)
                bboxs.append([id,bbox,detection.score])
                if draw :
                    img =  self.fancyDraw(img,bbox)  
                    cv2.putText(img,f'{int(detection.score[0]*100)} %',\
                        (bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        return img , bboxs            

    def fancyDraw(self,img,bbox,l=30,t=10) :
        x , y, w , h = bbox
        x1 , y1 = x+w , y+h
        cv2.rectangle(img,bbox,(0,255,0),1)
        #Top Left
        cv2.line(img,(x,y),(x+l,y),(0,255,0),t)
        cv2.line(img,(x,y),(x,y+l),(0,255,0),t)
        #Top Right
        cv2.line(img,(x1,y),(x1-l,y),(0,255,0),t)
        cv2.line(img,(x1,y),(x1,y+l),(0,255,0),t)
        #Bottom Left
        cv2.line(img,(x,y1),(x+l,y1),(0,255,0),t)
        cv2.line(img,(x,y1),(x,y1-l),(0,255,0),t)
        #Bottom Right
        cv2.line(img,(x1,y1),(x1-l,y1),(0,255,0),t)
        cv2.line(img,(x1,y1),(x1,y1-l),(0,255,0),t)
        return img

def main() :
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("Videos/vid2.mp4")

    cTime=0
    pTime=0

    detector = FaceDetector()
    while True:
        success , img = cap.read()
        img = cv2.flip(img,1)
        img , bboxs = detector.findFaces(img)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,f'FPS : {int(fps)}',(20,75),cv2.FONT_HERSHEY_COMPLEX,1,(4, 0, 246),3)
        cv2.imshow("Video",img)
        if(cv2.waitKey(10) == ord('d')) :
             break
        # cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()        

if __name__ == "__main__" :
    main()