import numpy as np
import time 
import cv2

UPPER_LIP = [13]
LOWER_LIP = [14]
LEFT_MOUTH_CORNER = [61]
RIGHT_MOUTH_CORNER = [291]

# Thresholds
YAWN_RATIO_UPPER_THRESHOLD = 0.6  # Upper limit for detecting a yawn
YAWN_RATIO_LOWER_THRESHOLD = 0.4  # Lower limit to reset the yawning state
ALERT_THRESHOLD = 3  # Number of yawns for an alert
ALERT_INTERVAL = 10  # Time interval in seconds
# ALERT_SOUND_DURATION = 15

# Initialize variables
yawn_counter = 0
YAWNING_STATUS  = ['YAWNING',"NOT_YAWNING"]
yawning = YAWNING_STATUS[1] # YAWNING
start_time = time.time()

class YawnDetection:

    def __init__(self):
        self.yawn_counter = 0
        self.start_time = time.time()
        self.YAWNING_STATUS =  ['YAWNING',"NOT_YAWNING"]
        self.yawnign = self.YAWNING_STATUS[1] 
    
    def getYawnStatusText(self,resultSetLandmark,image):
        height, width, _ = image.shape
        if resultSetLandmark.multi_face_landmarks:
            for face_landmarks in resultSetLandmark.multi_face_landmarks:
            # Extract the landmark coordinates
                landmarks = np.array([[lm.x * width, lm.y * height] for lm in face_landmarks.landmark])

                # Calculate mouth distances
                upper_lip = landmarks[UPPER_LIP[0]]
                lower_lip = landmarks[LOWER_LIP[0]]
                left_corner = landmarks[LEFT_MOUTH_CORNER[0]]
                right_corner = landmarks[RIGHT_MOUTH_CORNER[0]]

                vertical_distance = np.linalg.norm(upper_lip - lower_lip)
                horizontal_distance = np.linalg.norm(left_corner - right_corner) 

                yawn_ratio = vertical_distance / horizontal_distance

                if yawn_ratio > YAWN_RATIO_UPPER_THRESHOLD:
                    if not (self.yawning == self.YAWNING_STATUS[0]):
                        self.yawning = self.YAWNING_STATUS[0]
                        self.yawn_counter += 1
                elif yawn_ratio < YAWN_RATIO_LOWER_THRESHOLD:
                    self.yawning = self.YAWNING_STATUS[1]

                cv2.putText(image, f"Yawn Ratio: {yawn_ratio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(image, f"Yawn Count: {self.yawn_counter}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(image, f"Yawn Status: {self.yawnign}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        elapsed_time = time.time() - self.start_time
        if elapsed_time >= ALERT_INTERVAL :
            self.start_time = time.time()
            self.yawn_counter = 0

        return image,self.yawning



def getYawnStatus(result_landmarks,image) -> tuple:

    global yawn_counter,yawning,start_time

    height, width, _ = image.shape
    if result_landmarks.multi_face_landmarks:
        for face_landmarks in result_landmarks.multi_face_landmarks:
            # Extract the landmark coordinates
            landmarks = np.array([[lm.x * width, lm.y * height] for lm in face_landmarks.landmark])

            # Calculate mouth distances
            upper_lip = landmarks[UPPER_LIP[0]]
            lower_lip = landmarks[LOWER_LIP[0]]
            left_corner = landmarks[LEFT_MOUTH_CORNER[0]]
            right_corner = landmarks[RIGHT_MOUTH_CORNER[0]]

            vertical_distance = np.linalg.norm(upper_lip - lower_lip)
            horizontal_distance = np.linalg.norm(left_corner - right_corner) 

            yawn_ratio = vertical_distance / horizontal_distance

            if yawn_ratio > YAWN_RATIO_UPPER_THRESHOLD:
                if not yawning:
                    yawning = YAWNING_STATUS[0]
                    yawn_counter += 1
            elif yawn_ratio < YAWN_RATIO_LOWER_THRESHOLD:
                yawning = YAWNING_STATUS[1]

            cv2.putText(image, f"Yawn Ratio: {yawn_ratio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, f"Yawn Count: {yawn_counter}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Reset the timer and counter after ALERT_INTERVAL if sound hasn't been triggered
    elapsed_time = time.time() - start_time
    if elapsed_time >= ALERT_INTERVAL :
        start_time = time.time()
        yawn_counter = 0  # Reset the yawn count after 60 seconds if no alert
                # alert_played = YAWNING_STATUS[1]
            
        

    return image,yawning

