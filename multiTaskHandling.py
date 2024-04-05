import threading

import time,math
import pygame
import cv2

pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

OBJECT_STATUS = "EYE_ABSENT" 
CAUTION_LIMIT = 8
time_started = time.time()
count = 0.0

cv = cv2.VideoCapture("resources/simpleman.mp4")

face_cascade = cv2.CascadeClassifier("CascadeClassifiers/haarcascade_frontalface_default.xml")

def CounterClock():
    global OBJECT_STATUS
    global count
    global time_started

    while True:
        time_now = time.time()
        count = float(time_now)- float(time_started)
        print(math.floor(count))
        time.sleep(1)
        
        if OBJECT_STATUS == "EYE_PRESENT":
            time_started = time.time()
            count = 0.0
            print("Counter set to zero")
            print("[SAFE & SOUND]")


        if(count > CAUTION_LIMIT and OBJECT_STATUS == "EYE_ABSENT"): 
            pygame.mixer.music.load("resources/airplane-cockpit-alarm.mp3")
            print("[ACCIDENT HAZARD]")
            pygame.mixer.music.play()

        elif(count != 0):
            if ( count > 5 or count<CAUTION_LIMIT ): 
                pygame.mixer.music.load("resources/cabinchime.mp3")
                print("[CAUTION]")
                pygame.mixer.music.play()


def getVideofeed():
    global OBJECT_STATUS
    while True:
        Isframe,img = cv.read()
        gray_frame = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame,1.3,5)

        for x,y,w,h in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
            cv2.putText(img,"Hellow World!", (x,y-50),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)

        # Signals the current status of detection
        if len(faces) > 0:
            
            OBJECT_STATUS = "EYE_PRESENT"
            print(OBJECT_STATUS)
        else:
            OBJECT_STATUS =  "EYE_ABSENT"
            print(OBJECT_STATUS)
        
        if Isframe:
            img = cv2.resize(img,(800,500))
            cv2.imshow("Frame",img)

        
        # stops this process
        if cv2.waitKey(10) & 0xFF == ord('q'): 
            break
    

Thread1 = threading.Thread(target=getVideofeed)
Thread2 = threading.Thread(target=CounterClock)

Thread1.start()
Thread2.start()

Thread1.join()
Thread2.join()