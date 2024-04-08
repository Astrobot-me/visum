import cv2
import time
from faceMesh import GetFaceMesh

fm = GetFaceMesh(True,1,landmark=True)

cv = cv2.VideoCapture(0,cv2.CAP_DSHOW)

left_eye_coords = [362, 385, 387, 263, 373, 380]
#                    p2,  p6,  p4,  p1,  p3,  p5

right_eye_coords = [33,  160, 158, 136, 153, 144]
#                   p1  ,p4 , p6 , p2,  p5,  p3

while True:

    isFrame, img = cv.read()

    img, faces = fm.findFaceMesh(img,True)

    if faces:
        face = faces[0]
        for id in left_eye_coords:
            x,y = face[373]
            # left_eye_coords = [362, 385, 387, 263, 373, 380]
            #                    p2,  p6,  p4,  p1,  p3,  p5    
            cv2.circle(img,(x,y),2,(0,0,0),1,lineType=cv2.FILLED)
            

    if(isFrame):
        cv2.imshow(" Window",img)



    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break