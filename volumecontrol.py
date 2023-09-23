import cv2
import .HandDetectMod as htm
import numpy as np
import time, math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##########################
wCam , hCam = 640, 480
##########################

##########################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#print(volume.GetMute())
#print(volume.GetMasterVolumeLevel())
rng = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0.0, None)
##########################

cTime = pTime = 0

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1, detectionCon=0.8, trackCon=0.8)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findLms(img)
    if len(lmList) != 0:
        x1 , y1 = lmList[4][1], lmList[4][2]
        x2 , y2 = lmList[8][1], lmList[8][2]
        cx , cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img, (x1, y1), 10, (255, 0, 219), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 219), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 0, 219), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 219), 4)
        length = math.hypot((x2-x1),(y2-y1))
        vol = np.interp(length, [48,280], [rng[0], rng[1]])
        volBar = np.interp(length, [48,280], [365, 115])
        volPer = np.interp(length, [48,280], [0, 100])
        print(int(length), vol)
        if length <= 48:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img, (55, 115), (105, 365), (234,76,97), 3)
        cv2.rectangle(img, (55, int(volBar)), (105, 365), (234,76,97), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 430), cv2.FONT_HERSHEY_COMPLEX,
                    1.3, (255, 0, 0), 2)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #print(int(fps))
    cv2.putText(img, f'FPS: {int(fps)}', (30, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.imshow('Vol Control', img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        volume.SetMasterVolumeLevel(0.0, None)
        break
cap.release()
