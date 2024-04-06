import cv2
import time
import mediapipe as mp
import pygame

import cvzone
from faceMesh import GetFaceMesh



# idList = [22,23,25]
RIGHT_EYE_IDs = [33,  160, 158, 136, 153, 144]
#                p1  ,p4 , p6 , p2,  p5,  p3
temp_list = [144]
BLINK_COUNT = 0


# cv = cv2.VideoCapture("resources/Hello.mp4")
cv = cv2.VideoCapture(0,cv2.CAP_DSHOW)
meshDraw = GetFaceMesh()


while True:

    if cv.get(cv2.CAP_PROP_POS_FRAMES) == cv.get(cv2.CAP_PROP_FRAME_COUNT):
        cv.set(cv2.CAP_PROP_POS_FRAMES,0)

    isFrame,img = cv.read()

    if isFrame:
        img,faces = meshDraw.findFaceMesh(img,draw=True)

    if faces:
        face = faces[0]
        # print(face)
        for id in RIGHT_EYE_IDs:
            x,y = face[id]
            cv2.circle(img,center=(x,y),radius=2,color=(255,255,0),thickness=cv2.FILLED)
        
        p1 = face[33]
        p2 = face[133]
        p3 = face[144]
        p4 = face[160]
        p5 = face[153]
        p6 = face[158]

        upper_eyelid = [p2,p4,p6]
        lower_eyelid = [p1,p3,p5]

        

        length1,info,img = meshDraw.findDistance(p5,p6,img)
        length2,info,img = meshDraw.findDistance(p3,p4,img)
        length3,info,img = meshDraw.findDistance(p1,p2,img)

        print(length1,length2,length3)
#         RIGHT_EYE_IDs = [33,  160, 158, 133, 153, 144]
#                 p1  ,p4 , p6 , p2,  p5,  p3
        
        cv2.putText(img,str(BLINK_COUNT),(100,100),cv2.FONT_HERSHEY_PLAIN,color=(255,0,255),fontScale=2,thickness=2)
        #Calculating Ear Aspect Ratio 
        EAR_ASPECT_RATIO = (length2+length1)/(2*length3)
        print(EAR_ASPECT_RATIO)
        if EAR_ASPECT_RATIO < 0.220:
            BLINK_COUNT = BLINK_COUNT + 1
            print("EYE_CLOSED")
        else:
            print("EYE_OPEN")




    if isFrame:
        cv2.imshow("frame",img)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break