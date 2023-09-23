import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode = False, maxHands=2, modelCom=1,detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComp = modelCom
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.maxHands, self.modelComp, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS,
                                               connection_drawing_spec=
                                               self.mpDraw.DrawingSpec((233,43,5),thickness=3))
        return img

    def findLms(self, img, handNo=0, drawCir=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,l
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if drawCir:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 219), cv2.FILLED)
        return lmList

def main():
    cTime = 0
    pTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findLms(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
        cv2.imshow("Result", img)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    cap.release()

if __name__ == '__main__':
    main()
