import cv2
import time
import mediapipe as mp
import pygame


from faceMesh import GetFaceMesh

ear = [0.262,0.256,0.255,0.254,0.262]

# idList = [22,23,25]
RIGHT_EYE_IDs = [33,  160, 158, 136, 153, 144]
#                p1  ,p4 , p6 , p2,  p5,  p3

LEFT_EYE_IDs = [362, 385, 387, 263, 373, 380]
#               p2,  p6,  p4,  p1,  p3,  p5  

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
        
        for id in LEFT_EYE_IDs:
            x,y = face[id]
            cv2.circle(img,center=(x,y),radius=2,color=(255,255,0),thickness=cv2.FILLED)

        # Right Eye
        p1_RIGHT = face[33]
        p2_RIGHT = face[133]
        p3_RIGHT = face[144]
        p4_RIGHT = face[160]
        p5_RIGHT = face[153]
        p6_RIGHT = face[158]

        # Right EyePoint Distance Calculation
        RIGHT_length1,info,img = meshDraw.findDistance(p5_RIGHT,p6_RIGHT,img)
        RIGHT_length2,info,img = meshDraw.findDistance(p3_RIGHT,p4_RIGHT,img)
        RIGHT_length3,info,img = meshDraw.findDistance(p2_RIGHT,p1_RIGHT,img)

        print(f"Right Eye L1: {RIGHT_length1},L2: {RIGHT_length2},L3: {RIGHT_length3}")
        #RIGHT_EYE_IDs = [33,  160, 158, 133, 153, 144]
        #                 p1  ,p4 , p6 , p2,  p5,  p3


        # LEFT Eye FaceLand Mark Points
        p1_LEFT = face[263]
        p2_LEFT = face[362]
        p3_LEFT = face[373]
        p4_LEFT = face[387]
        p5_LEFT = face[380]
        p6_LEFT = face[385]
        
        # Left EyePoint Distance Calculation

        LEFT_length1,info,img = meshDraw.findDistance(p5_LEFT,p6_LEFT,img)
        LEFT_length2,info,img = meshDraw.findDistance(p3_LEFT,p4_LEFT,img)
        LEFT_length3,info,img = meshDraw.findDistance(p2_LEFT,p1_LEFT,img)

        print(f"Left Eye L1: {LEFT_length1},L2: {LEFT_length2},L3: {LEFT_length3}")
        
        # cv2.putText(img,str(BLINK_COUNT),(100,100),cv2.FONT_HERSHEY_PLAIN,color=(255,0,255),fontScale=2,thickness=2)
        

        print("")

        #Calculating Ear Aspect Ratio 
        EAR_ASPECT_RATIO_RIGHT = (RIGHT_length2+RIGHT_length1)/(2*RIGHT_length3)
        print(f"Right Eye EAR: {EAR_ASPECT_RATIO_RIGHT}")

         #Calculating Ear Aspect Ratio 
        EAR_ASPECT_RATIO_LEFT = (LEFT_length2+LEFT_length1)/(2*LEFT_length3)
        print(f"Left Eye EAR: {EAR_ASPECT_RATIO_LEFT}")

        AVERAGE_EAR = (EAR_ASPECT_RATIO_LEFT+EAR_ASPECT_RATIO_RIGHT)/2
        

        ear.append(AVERAGE_EAR)

        if(len(ear)>5):
            ear.pop(0)

        print(ear)

        print("")

        

        newEAR = sum(ear)/len(ear)

        print(f"Avarage EAR : {newEAR}")

        print("")




        if newEAR < 0.260:
            # BLINK_COUNT = BLINK_COUNT + 1
            print("EYE_CLOSED")
        else:
            print("EYE_OPEN")




    if isFrame:
        cv2.imshow("frame",img)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


ear = [0.262,0.256,0.255,0.254,0.262]