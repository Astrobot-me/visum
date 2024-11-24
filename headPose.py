import cv2
import numpy
import pandas as pd

pitch_array = []
yaw_array = []

def getHeadTilt(face_ladmarks,image):
    # img = cv2.imread(image,1)
    print("Image shape : ",image.shape)
    img_h, img_w,img_channel = image.shape
    if face_ladmarks.multi_face_landmarks:
       
        for landmarks in face_ladmarks.multi_face_landmarks:
            face_2dCords = []
            face_3dCords = []
            
            for index,lnd in enumerate(landmarks.landmark):
                # 1,33,263,61,241,144 : previous 
                # 1,152,263,33,61,291
                if  index == 1 or  index == 33 or  index == 263 or  index == 61 or  index == 291 or  index == 152:
                    if  index == 1:
                        Nose_2dCords = (int(lnd.x * img_w), int(lnd.y * img_h))
                        Nose_3dCords = (lnd.x * img_w, lnd.y * img_h,lnd.z * 3000)
                    
                    x,y = int(lnd.x * img_w), int(lnd.y * img_h)
                    face_2dCords.append([x,y])
                    face_3dCords.append([x,y,lnd.z])
    else:
        return image
    print("Face 2d Cords:",face_2dCords)
    print("Face 3d Cords: ",face_3dCords)

    face_2dCords = numpy.array(face_2dCords,dtype=numpy.float64)
    face_3dCords = numpy.array(face_3dCords,dtype=numpy.float64)


    focal_length = 1 * img_w
    cameraMatrix = numpy.array([[
        focal_length,0,img_h/2
    ],[
        0,focal_length,img_w/2
    ],[
        0,0,1
    ]],dtype=numpy.float64)

    distortionMatrix = numpy.zeros((4,1))
    isTranslate, rvec, tvec = cv2.solvePnP(face_3dCords,face_2dCords,cameraMatrix,distortionMatrix) 
    rotationMatrix, _ = cv2.Rodrigues(rvec)

    rotationAngles,mtxR,mtxQ,qx,qy,qz = cv2.RQDecomp3x3(rotationMatrix)
    '''
    (
        (rx, ry, rz), # Rotation angles around the x, y, z axes in radians
        mtxR,         # Original rotation matrix
        mtxQ,         # Upper triangular matrix (related to scaling)
        qx,           # Rotation matrix around the x-axis
        qy,           # Rotation matrix around the y-axis
        qz            # Rotation matrix around the z-axis
    )

    '''
    pitch= rotationAngles[0]
    yaw = rotationAngles[1]
    roll = rotationAngles[2]

    # # Normalized Values of pitch,yaw & roll
    pitch = pitch * 360
    yaw = yaw * 360
    roll = roll * 360
    
    pitch,yaw = calculateMovingAvarage(pitch,yaw)

    CurrentStateText1,CurrentStateText2 = getTiltStatus(pitch,yaw,roll)

    if(CurrentStateText1!=None):
        cv2.putText(image,CurrentStateText1, (200,30),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)
    if(CurrentStateText2 != None):
        cv2.putText(image,CurrentStateText2, (200,300),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)


    print(f"Pitch :{pitch}, Yaw: {yaw}, Roll:{roll}")
    axis = numpy.float32([[10, 0, 0], [0, 10, 0], [0, 0, 10]])
    nose3d_realization,_ = cv2.projectPoints(axis,rvec,tvec,cameraMatrix,distortionMatrix)
   
    #dynamic Scaling of head pose line 
    base_scaling_factor = 10
    distance_from_camera = tvec[2][0]

    dynamic_scaling_factor = base_scaling_factor/max(1,distance_from_camera/1000)
    
    if nose3d_realization is not None:
        # nose_point = (int(landmarks[1].x * img_w), int(landmarks[1].y * img_h))
        
        x_axis = (int(nose3d_realization[0][0][0]), int(nose3d_realization[0][0][1]))
        y_axis = (int(nose3d_realization[1][0][0]), int(nose3d_realization[1][0][1]))
        z_axis = (int(nose3d_realization[2][0][0]), int(nose3d_realization[2][0][1]))


         # Ensure nose3d_realization has enough points before accessing them
        if len(nose3d_realization) >= 3:
            # Draw the X, Y, and Z axes
            cv2.line(image, Nose_2dCords,x_axis , (0, 0, 255), 3)  # X-axis (red)
            cv2.line(image, Nose_2dCords,y_axis , (0, 255, 0), 3)  # Y-axis (green)
            cv2.line(image, Nose_2dCords, z_axis, (255, 0, 0), 3)  # Z-axis (blue)


    # Display the nose direction    
    # p1 = (int(Nose_2dCords[0]), int(Nose_2dCords[1]))
    # p2 = (int(Nose_2dCords[0] + y * dynamic_scaling_factor), int(Nose_2dCords[1] - x * dynamic_scaling_factor))

    # p1 = (int(nose3d_realization[0][0][0]), int(nose3d_realization[0][0][1]))
    # p2 = (int(p1[0] + y * 10), int(p1[1] - x * 10))



    # cv2.line(image, p1, p2, (255, 0, 0), 3)

    # Add the text on the image
    cv2.putText(image, "x: " + str(numpy.round(pitch, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, "y: " + str(numpy.round(yaw, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, "z: " + str(numpy.round(roll, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return image




def getTiltStatus(pitch = 0 ,yaw = 0 ,roll = 0):
    
    FACE_STATES_PITCH = ['LOOKING_UP','FACE_UP','LOOKING_DOWN','FACE_DOWN']
    FACE_STATES_YAW = ['LOOKING_LEFT ','FACE_LEFT','LOOKING_RIGHT','FACE_RIGHT']
    COMBINED_STATES = ['TOP_LEFT',"TOP_RIGHT","BOTTOM_LEFT","BOTTOM_RIGHT"]

    CURRENT_STATE = "NO_STATE"
    CURRENT_COMBINED_STATE = "N0_STATE"
    
   
    
    if(pitch >=  13.5 and pitch < 19):
        CURRENT_STATE = FACE_STATES_PITCH[0]
    elif(pitch >= 19):
        CURRENT_STATE = FACE_STATES_PITCH[1] 
    elif(pitch <= -4 and pitch > -8 ):
        CURRENT_STATE = FACE_STATES_PITCH[2]
    elif(pitch < -8):
        CURRENT_STATE = FACE_STATES_PITCH[3]

   
    elif(yaw <= -7 and yaw > -15):
        CURRENT_STATE = FACE_STATES_YAW[2]
    elif(yaw < -15):
        CURRENT_STATE = FACE_STATES_YAW[3]
    elif(yaw >= 10 and yaw < 14):
        CURRENT_STATE = FACE_STATES_YAW[0]
    elif(yaw > 14):
        CURRENT_STATE = FACE_STATES_YAW[1]

            
    # combined state

    if(pitch >= 18.5 and yaw >= 10):
        CURRENT_COMBINED_STATE = COMBINED_STATES[0]
    elif(pitch >= 18.5 and yaw < -12):
        CURRENT_COMBINED_STATE = COMBINED_STATES[1]
    elif(pitch<-5 and yaw >= 8):
        CURRENT_COMBINED_STATE = COMBINED_STATES[2]
    elif(pitch<-6 and yaw <= -10):
        CURRENT_COMBINED_STATE = COMBINED_STATES[3]

    return CURRENT_STATE,CURRENT_COMBINED_STATE
    

        
        
# Implement Moving Average function 

def calculateMovingAvarage(pitch:float , yaw:float ) -> tuple: 
    
    global pitch_array,yaw_array
    # roll_array = []

    pitch_array.append(pitch)
    yaw_array.append(yaw)
    # roll_array.append(roll)

    window_size = 6

    if(len(pitch_array)>window_size):
        pitch_array.pop(0)

    if(len(yaw_array)>window_size):
        yaw_array.pop(0)

    # if(len(roll_array)>window_size):
    #     roll_array.pop()

    pitch_series = pd.Series(pitch_array)  
    yaw_series = pd.Series(yaw_array)  
    # roll_series = pd.Series(roll_array)  

    
    pitch_SMA = pitch_series.rolling(window_size).mean().iloc[-1] if len(pitch_array)>=window_size else 0
    yaw_SMA = yaw_series.rolling(window_size).mean().iloc[-1] if len(yaw_array)>=window_size else 0
        # roll_SMA = roll_series.rolling(window_size).mean() 


    print(f"Rolling Mean - pitch: {pitch_SMA}, yaw: {yaw_SMA}")
    return pitch_SMA,yaw_SMA



