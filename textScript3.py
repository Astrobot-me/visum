import datetime,math
import time
import pygame
import cv2 


pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

# Config Settings
cv = cv2.VideoCapture("resources/simpleman.mp4")

face_cascade = cv2.CascadeClassifier("CascadeClassifiers/haarcascade_frontalface_default.xml")

OBJECT_STATUS = "EYE_ABSENT" 
CAUTION_LIMIT = 10
time_started = time.time()
count = 0.0


while True:
    time_now = time.time()
    count = float(time_now)- float(time_started)
    print(math.floor(count))
    # time.sleep(1)

    Isframe,img = cv.read()
    gray_frame = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
    
    if len(faces) > 0:
        OBJECT_STATUS = "EYE_PRESENT"
    else:
         OBJECT_STATUS =  "EYE_ABSENT"

    for x,y,w,h in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
        cv2.putText(img,"Hellow World!", (x,y-50),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)



    if Isframe:
            img = cv2.resize(img,(800,500))
            cv2.imshow("Frame",img)

    if cv2.waitKey(10) & 0xFF == ord('q'): 
            break
                        

                            
    

    if(count > CAUTION_LIMIT and OBJECT_STATUS == "EYE_ABSENT"): 
        pygame.mixer.music.load("resources/airplane-cockpit-alarm.mp3")
        print("[ACCIDENT HAZARD] : Please Drive the Vehicle")
        pygame.mixer.music.play()
        

    elif ( count > 5 or count<CAUTION_LIMIT ): 
        pygame.mixer.music.load("resources/cabinchime.mp3")
        print("[CAUTION] : Please focus")
        pygame.mixer.music.play()