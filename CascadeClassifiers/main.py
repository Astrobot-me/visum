import cv2, numpy
import pygame 

videos_stream = cv2.VideoCapture(0,cv2.CAP_DSHOW)
print(f" Video Opening Status: {videos_stream.isOpened()}")


face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade  = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")
# eye_cascade  = cv2.CascadeClassifier("haarcascade_eye.xml")
while True: 
   
    frame_status , frame = videos_stream.read() # Boolean & actual Frame
    # pointA = (200,200)
    # pointB = (450,450)
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    print(f"Image size:  {gray_frame}")

    faces = face_cascade.detectMultiScale(gray_frame,1.3,5) #return tuple
    for x,y,w,h in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
        cv2.putText(frame,"Hellow World!", (x,y-50),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255))

        face_crop = gray_frame[y:y+h,x:x+w]
        color_face_crop = frame[y:y+h, x:x+w]
        eye_locations = eye_cascade.detectMultiScale(face_crop)

    

        for p,q,r,s in eye_locations:
            cv2.rectangle(face_crop, (p,q), (p+r,q+s), (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
            cv2.rectangle(color_face_crop, (p,q), (p+r,q+s), (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)
        
        

    
    # cv2.imshow('Image Line', frame)


    # print(f"frame Available : {frame_status}")

    if frame_status:
        cv2.imshow("frame",frame)
        cv2.imshow("gray",face_crop)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


videos_stream.release()
cv2.destroyAllWindows()