from threading import *
import threading
import pygame as pg
import time 
import random


pg.mixer.init()

status = "OPEN"

def objStatus():
    global status
    while True:
        statuses = ["OPEN","CLOSED","Normal"]
        status = random.choice(statuses)
        print(f"Status Changed to : {status}")
        time.sleep(10)
        


def playAudio1():
        global status
        while True:
            if(status=="CLOSED"):
                print("Playing Audio 1....");
                pg.mixer.music.load("resources/airplane-cockpit-alarm.mp3")
                pg.mixer.music.set_volume(1.0)
                pg.mixer.music.play()
                time.sleep(1)
            elif status == "Normal":
                 print("Condition is Nominal")
            else:
                print("Playing Audio 2....");
                pg.mixer.music.load("resources/cabinchime.mp3")
                pg.mixer.music.set_volume(1.0)
                pg.mixer.music.play()
                time.sleep(1)
                 
        







if __name__ == "__main__" :
    t1 = threading.Thread(target=objStatus)
    t2 = threading.Thread(target=playAudio1)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
