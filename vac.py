import math
import time
from ctypes import POINTER, cast

import cv2
import handtrackingmodule as htm
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# #########################
wCam,hCam=1280,720
# ############################


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0

detector=htm.handDetector(detectionCon=0.7)
devices  =AudioUtilities.GetSpeakers()
interface =devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]


while True:
    isTrue,img=cap.read()
    img= detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        length = math.hypot(x2-x2,y2-y1)
        #print()

        vol =np.interp(length,[50,300],[minVol,maxVol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol,None)

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

        #handrange


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,
        (255,0,255),3)

    cv2.imshow('video',img)

    if cv2.waitKey(20) & 0xFF==ord('d'):#if letter d is pressed stop video
        break
cv2.waitKey(1)