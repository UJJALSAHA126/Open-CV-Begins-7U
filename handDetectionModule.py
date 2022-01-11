import cv2 as cv
import mediapipe as mp


class HandDetector():
    fingerTips = {4, 8, 12, 16, 20}

    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackConfidence=0.5):
        self.__mode = mode
        self.__maxHands = maxHands
        self.__detectionConfidence = detectionConfidence
        self.__trackConfidence = trackConfidence
        self.__mpHands = mp.solutions.mediapipe.python.solutions.hands
        self.__hands = self.__mpHands.Hands(
            self.__mode, self.__maxHands, 1, self.__detectionConfidence, self.__trackConfidence)
        self.__mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils

    def findFingerPositions(self, img, fingerPoints=fingerTips,
                            handNo=-1, draw=True, color=(255, 0, 0),
                            drawFinterTips=False):
        self.__results = self.__hands.process(
            cv.cvtColor(img, cv.COLOR_BGR2RGB))

        positionalLandmark = []

        if self.__results.multi_hand_landmarks:
            handLms = self.__results.multi_hand_landmarks

            for hNo, handLm in enumerate(handLms):
                if(handNo != -1 and handNo != hNo):
                    continue
                if draw:
                    self.__mpDraw.draw_landmarks(img, handLm,
                                                 self.__mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(handLm.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    positionalLandmark.append([hNo, [id, cx, cy]])
                    if drawFinterTips and (id in fingerPoints):
                        cv.circle(img, (cx, cy), 10, color, cv.FILLED)
            return positionalLandmark, handLms

        return None, None


if __name__ == '__main__':
    mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils
    mpHands = mp.solutions.mediapipe.python.solutions.hands
    hdm = HandDetector()
    video = cv.VideoCapture(0)
    while True:
        b, img = video.read()
        img = cv.flip(img, 1)
        _, lmList = hdm.findFingerPositions(img, draw=False)
        if lmList is not None:
            for lm in lmList:
                mpDraw.draw_landmarks(img, lm, mpHands.HAND_CONNECTIONS)
        cv.imshow('Hand', img)
        # if(len(lmList) > 0):
        #     print(lmList[4])
        if cv.waitKey(1) == ord('d'):
            break
