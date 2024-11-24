import mediapipe as mp 
import cv2

cam = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils

pose = mpPose.Pose()

while True:
    isImg,img  = cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    if(isImg):
        result = pose.process(imgRGB)
        if(result.pose_landmarks):
            pass
        print(result) 
        cv2.imshow("Img",img)

    cv2.waitKey(1)