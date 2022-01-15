import cv2 
import time
import mediapipe as mp

# cap = cv2.VideoCapture("Videos/vid2.mp4")
cap = cv2.VideoCapture(0)

cTime=0
pTime=0

myFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = myFaceDetection.FaceDetection()

while True:
    success , img = cap.read()
    img = cv2.flip(img,1)
    imRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imRGB)
    print(results)

    if results.detections :
        for id , detection in enumerate(results.detections) :
            # mpDraw.draw_detection(img,detection)
            # print(id,detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            ih ,iw, ic = img.shape
            bbox= int(bboxC.xmin * iw) , int(bboxC.ymin * ih) ,\
                int(bboxC.width * iw) , int(bboxC.height * ih)
            cv2.rectangle(img,bbox,(0,255,0),3)    
            cv2.putText(img,f'{int(detection.score[0]*100)} %',\
                (bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS : {int(fps)}',(20,75),cv2.FONT_HERSHEY_COMPLEX,1,(4, 0, 246),3)
    cv2.imshow("Video",img)
    if(cv2.waitKey(10) == ord('d')) :
        break
    