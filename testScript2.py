import cv2 

class Videofeed: 

    def __init__(self, path):
        self.pathinDirectory = path

    def getVideoFeed(self):

        try:
            cv = cv2.VideoCapture(self.pathinDirectory)


            while True:
                
                Isframe,img = cv.read()
                if Isframe:
                    img = cv2.resize(img,(800,500))
                    cv2.imshow("Frame",img)

                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break
                
        except Exception:
            print(Exception)
