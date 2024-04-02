import datetime,math
import time
import pygame

pygame.mixer.init()

pygame.mixer.music.set_volume(1.0)

status = "EYE_ABSENT" 
# status = "EYE_PRESENT" 

# time_started = datetime.datetime.now()
time_started = time.time()
count = 0.0
while True:
    time_now = time.time()
    # print(time.strftime("%S"))
    count = float(time_now)- float(time_started)
    print(math.floor(count))
    time.sleep(1)

    if(count > 10 and status == "EYE_ABSENT"): 
        pygame.mixer.music.load("airplane-cockpit-alarm.mp3")
        print("[ACCIDENT HAZARD] : Please Drive the Vehicle")
        pygame.mixer.music.play()

    elif ( count > 5 or count<10 ): 
        pygame.mixer.music.load("cabinchime.mp3")
        print("[CAUTION] : Please focus")
        pygame.mixer.music.play()
        
    