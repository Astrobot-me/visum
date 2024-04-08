import datetime,math
import time
import pygame
from testScript2 import Videofeed
import threading

# VideoStream = Videofeed("resources/vid1.mp4")

pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

OBJECT_STATUS = "EYE_ABSENT" 
CAUTION_LIMIT = 20
# status = "EYE_PRESENT" 


# x = threading.Thread(target=VideoStream.getVideoFeed(), args=(1,), daemon=True)


# time_started = datetime.datetime.now()
time_started = time.time()
count = 0.0

# x.start()


while True:
    time_now = time.time()
    # print(time.strftime("%S"))
    count = float(time_now)- float(time_started)
    print(math.floor(count))
    time.sleep(1)

    # Getting Video Feed
    # VideoStream.getVideoFeed()
    

    if(count > CAUTION_LIMIT and OBJECT_STATUS == "EYE_ABSENT"): 
        pygame.mixer.music.load("resources/airplane-cockpit-alarm.mp3")
        print("[ACCIDENT HAZARD] : Please Drive the Vehicle")
        pygame.mixer.music.play()

    elif ( count > 5 or count<CAUTION_LIMIT ): 
        pygame.mixer.music.load("resources/cabinchime.mp3")
        print("[CAUTION] : Please focus")
        pygame.mixer.music.play()
        
    