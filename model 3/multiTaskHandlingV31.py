import cv2
import time,math
import mediapipe as mp
import pygame
from faceMesh import GetFaceMesh
import openpyxl
import threading
import serial

pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

ser = serial.Serial('COM3', 9600)

excel_obj = openpyxl.load_workbook("datalog4.xlsx")
datasheet = excel_obj.active
sheet_index = 4
# idList = [22,23,25]

# program setting values : PSV
OBJECT_STATUS = "EYE_ABSENT" 
CAUTION_LIMIT = 4
time_started = time.time()
count = 0.0
NOSE_THRESHOLD = 30
RIGHTEYE_THRESHOLD = 20
LEFTEYE_THRESHOLD = 20
EAR_THRESHOLD = 0.270
ear = [0.262,0.256,0.255,0.254,0.262]
RIGHT_EYE_IDs = [33,  160, 158, 136, 153, 144]
LEFT_EYE_IDs = [362, 385, 387, 263, 373, 380]


meshDraw = GetFaceMesh()
cv = cv2.VideoCapture(0,cv2.CAP_DSHOW)


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
            state = 1
            ser.write(str(state).encode())  # Send the state to Arduino
            print(f'Sent state {state} to Arduino')
            print("Counter set to zero")
            print("[SAFE & SOUND]")


        if(count > CAUTION_LIMIT and OBJECT_STATUS == "EYE_ABSENT"): 
            pygame.mixer.music.load("resources/airplane-cockpit-alarm.mp3")
            state = 3
            ser.write(str(state).encode())  # Send the state to Arduino
            print(f'Sent state {state} to Arduino')
            print("[ACCIDENT HAZARD]")
            pygame.mixer.music.play()

        elif(count != 0):
            if ( count > 5 or count<CAUTION_LIMIT ): 
                pygame.mixer.music.load("resources/cabinchime.mp3")
                state = 2
                ser.write(str(state).encode())  # Send the state to Arduino
                print(f'Sent state {state} to Arduino')
                print("[CAUTION]")
                pygame.mixer.music.play()

def computeVideoEAR():
    
    global OBJECT_STATUS
    global count
    global time_started
    global ear
    global RIGHT_EYE_IDs
    global LEFT_EYE_IDs
    global datasheet,sheet_index

    while True:

        # if cv.get(cv2.CAP_PROP_POS_FRAMES) == cv.get(cv2.CAP_PROP_FRAME_COUNT):
        #     cv.set(cv2.CAP_PROP_POS_FRAMES,0)

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



            N1 = face[219]
            N2 = face[439]
            
            # Left EyePoint Distance Calculation

            LEFT_length1,info,img = meshDraw.findDistance(p5_LEFT,p6_LEFT,img)
            LEFT_length2,info,img = meshDraw.findDistance(p3_LEFT,p4_LEFT,img)
            LEFT_length3,info,img = meshDraw.findDistance(p2_LEFT,p1_LEFT,img)

            print(f"Left Eye L1: {LEFT_length1},L2: {LEFT_length2},L3: {LEFT_length3}")
            
            # cv2.putText(img,str(BLINK_COUNT),(100,100),cv2.FONT_HERSHEY_PLAIN,color=(255,0,255),fontScale=2,thickness=2)
            Nose_length,info, img = meshDraw.findDistance(N1,N2,img) 

            print(f"Nose length : {Nose_length}")

            if RIGHT_length3 <= 20 or Nose_length < 30:
                print("FACE TURNED RIGHT")
                cv2.putText(img,"FACE TURNED RIGHT", (200,100),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)

            elif LEFT_length3 <=20 or Nose_length < 30:
                print("FACE TURNED LEFT")
                cv2.putText(img,"FACE TURNED LEFT", (200,100),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)
            
            else:
                cv2.putText(img,"FACE STRAIGHT", (200,100),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,255,0),thickness=2)
                

            #Calculating Ear Aspect Ratio 
            EAR_ASPECT_RATIO_RIGHT = ((RIGHT_length2+RIGHT_length1)/2)/(RIGHT_length3)
            print(f"Right Eye EAR: {EAR_ASPECT_RATIO_RIGHT}")

            #Calculating Ear Aspect Ratio 
            EAR_ASPECT_RATIO_LEFT = ((LEFT_length2+LEFT_length1)/2)/(LEFT_length3)
            print(f"Left Eye EAR: {EAR_ASPECT_RATIO_LEFT}")

            AVERAGE_EAR = (EAR_ASPECT_RATIO_LEFT+EAR_ASPECT_RATIO_RIGHT)/2
            

            ear.append(AVERAGE_EAR)

            if(len(ear)>5):
                ear.pop(0)

            print(ear)

            print("")

            

            newEAR = sum(ear)/len(ear)

            # try:
            #     # writeData(RIGHT_length1,RIGHT_length2,RIGHT_length3,EAR_ASPECT_RATIO_RIGHT,LEFT_length1,LEFT_length2,LEFT_length3,EAR_ASPECT_RATIO_LEFT,AVERAGE_EAR,newEAR,Nose_length)
            #     # sheet_index = sheet_index+1
            # except:
            #     pass

            print(f"Avarage EAR : {newEAR}")

            print("")




            if newEAR < EAR_THRESHOLD:
                # BLINK_COUNT = BLINK_COUNT + 1
                OBJECT_STATUS = "EYE_ABSENT"
                print(f"STATUS: {OBJECT_STATUS}")
            else:
                OBJECT_STATUS = "EYE_PRESENT"
                print(f"STATUS: {OBJECT_STATUS}")





        if isFrame:
            cv2.imshow("frame",img)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def writeData(R_l1,R_l2,R_l3,R_EAR,L_l1,L_l2,L_l3,L_EAR,A_EAR,List_EAR,nose):
    # writes data to datalog Excel file
    global sheet_index
    global datasheet

    try:
        datasheet[f"A{sheet_index}"] = R_l1;
        datasheet[f"B{sheet_index}"] = R_l2;
        datasheet[f"C{sheet_index}"] = R_l3;
        datasheet[f"D{sheet_index}"] = R_EAR;

        datasheet[f"E{sheet_index}"] = L_l1;
        datasheet[f"F{sheet_index}"] = L_l2;
        datasheet[f"G{sheet_index}"] = L_l3;
        datasheet[f"H{sheet_index}"] = L_EAR;

        datasheet[f"I{sheet_index}"] = A_EAR;
        datasheet[f"J{sheet_index}"] = List_EAR;


        datasheet[f"K{sheet_index}"] = nose;
    
    except(Exception):
        print(Exception)

    excel_obj.save("datalog4.xlsx")






    


Thread1 = threading.Thread(target=computeVideoEAR)
Thread2 = threading.Thread(target=CounterClock)

Thread1.start()
Thread2.start()

Thread1.join()
Thread2.join()