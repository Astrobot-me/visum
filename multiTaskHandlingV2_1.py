import threading

import time,math
import pygame
import cv2

pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

index = 0



OBJECT_STATUS = "EYE_ABSENT" 
CAUTION_LIMIT = 8
time_started = time.time()
count = 0.0
LABEL = "SAFE"
COLOR = (51, 134, 0)

# cv = cv2.VideoCapture("resources/simpleman.mp4")
cv = cv2.VideoCapture(index,cv2.CAP_DSHOW)

# Face Detection Model
face_cascade = cv2.CascadeClassifier("CascadeClassifiers/haarcascade_frontalface_default.xml")

#Eye-Detection Model
eye_cascade  = cv2.CascadeClassifier("CascadeClassifiers/haarcascade_eye_tree_eyeglasses.xml")

def CounterClock():
    global OBJECT_STATUS
    global count
    global time_started
    global LABEL,COLOR

    while True:
        time_now = time.time()
        count = float(time_now)- float(time_started)
        print(math.floor(count))
        time.sleep(1)
        
        if OBJECT_STATUS == "EYE_PRESENT":
            time_started = time.time()
            count = 0.0
            LABEL = "SAFE"
            COLOR = (51, 134, 0)
            print("Counter set to zero")
            print("[SAFE & SOUND]")


        if(count > CAUTION_LIMIT and OBJECT_STATUS == "EYE_ABSENT"): 
            pygame.mixer.music.load("resources/airplane-cockpit-alarm.mp3")
            LABEL = "ACCIDENT HAZARD"
            COLOR = (0,0,255)
            print("[ACCIDENT HAZARD]")
            pygame.mixer.music.play()

        elif(count != 0):
            if ( count > 5 or count<CAUTION_LIMIT ): 
                pygame.mixer.music.load("resources/cabinchime.mp3")
                LABEL = "CAUTION"
                COLOR = (255,0,0)
                print("[CAUTION]")
                pygame.mixer.music.play()


def getVideofeed():
    global OBJECT_STATUS
    global COLOR

    while True:
        BACKGROUND_SKELETON = cv2.imread("resources/skeletons/background_skeletonv2_1.png")
        Isframe,img = cv.read()
        gray_frame = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
        # eye_locations = []
        for x,y,w,h in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0, 255, 0), thickness=3, lineType=cv2.LINE_AA)
            cv2.putText(img,"I'm a Car Driver", (x,y-50),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)

            face_crop = gray_frame[y:y+h,x:x+w]
            color_face_crop = img[y:y+h, x:x+w]
            eye_locations = eye_cascade.detectMultiScale(face_crop)

            for p,q,r,s in eye_locations:
                cv2.rectangle(color_face_crop, (p,q), (p+r,q+s), (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)

        # Signals the current status of detection
        if len(eye_locations) > 0:
            
            OBJECT_STATUS = "EYE_PRESENT"
            print(OBJECT_STATUS)
        else:
            OBJECT_STATUS =  "EYE_ABSENT"
            print(OBJECT_STATUS)
        
        if Isframe:
            # img = cv2.resize(img,(800,500))
            time = round(count,4)
            BACKGROUND_SKELETON[200:200+img.shape[0], 58:58+img.shape[1]] = img

            cv2.putText(BACKGROUND_SKELETON, LABEL, (796, 323), cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=COLOR, thickness=2)

            cv2.putText(BACKGROUND_SKELETON, str(time),(825, 585), cv2.FONT_HERSHEY_PLAIN, fontScale=2.5, color=COLOR, thickness=2)

            cv2.putText(BACKGROUND_SKELETON, "Sec",(825, 620), cv2.FONT_HERSHEY_PLAIN, fontScale=1.8, color=COLOR, thickness=2)
            cv2.imshow("Accident Prevention System using Computer Vision",BACKGROUND_SKELETON)

        
        # stops this process
        if cv2.waitKey(10) & 0xFF == ord('q'): 
            break
    

Thread1 = threading.Thread(target=getVideofeed)
Thread2 = threading.Thread(target=CounterClock)

Thread1.start()
Thread2.start()

Thread1.join()
Thread2.join()