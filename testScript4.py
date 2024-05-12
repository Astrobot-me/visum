import cv2

import matplotlib.pyplot as plt
import random, datetime

import cvzone

from cvzone import PlotModule


live_plot = PlotModule.LivePlot(w=400,h=480, yLimit=[0, 100], interval=0.1)

while True:
    rand_num = random.randint(-3,3) 
    imgplot = live_plot.update(rand_num)

    cv2.imshow("Image", imgplot)
    tim = datetime.datetime.now()
    print(tim)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break






# image = cv2.imread('Script Lab/background_interface.png')


# if image is not None:
    
#     cv2.putText(image,"0.260", (80,333),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=2,color=(0,0,0),thickness=3,lineType=cv2.LINE_8) # mean
    
#     cv2.putText(image,"0.260", (80,513),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=2,color=(0,0,0),thickness=3,lineType=cv2.LINE_8) # left

#     cv2.putText(image,"0.260", (80,693),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=2,color=(0,0,0),thickness=3,lineType=cv2.LINE_8) # right

#     cv2.putText(image,"Right", (1052,246),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=2,color=(0,0,256),thickness=3,lineType=cv2.LINE_8) # orientation

#     cv2.putText(image,"ACCIDENT HAZARD", (1052,446),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.5,color=(256,0,0),thickness=3,lineType=cv2.LINE_8) # status

#     cv2.putText(image,"2.356", (1062,600),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.5,color=(256,0,0),thickness=3,lineType=cv2.LINE_8) # clock

#     cv2.putText(image,"CONNECTED", (1042,730),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.2,color=(105,236,25),thickness=2,lineType=cv2.LINE_8) # clock

#     cv2.putText(image,"Today at 7:10 PM 00:00:00", (550,760),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1.2,color=(44,116,0),thickness=2,lineType=cv2.LINE_4) # STA-LOG1
#     cv2.putText(image,"Today at 7:10 PM 00:00:00", (550,780),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1.2,color=(44,116,0),thickness=2,lineType=cv2.LINE_4) # STA_LOG2


    
#     cv2.imshow('Image', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("Image not found or could not be loaded.")


