import cv2
import mediapipe
import math


class GetFaceMesh:

    def __init__(self, staticMode=False, maxFaces=1, minDetectionCon=0.5, minTrackCon=0.5,landmark=False):
    
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon
        self.landmark = landmark

        self.mpDraw = mediapipe.solutions.drawing_utils
        self.mpFaceMesh = mediapipe.solutions.face_mesh

        self.faceMesh = self.mpFaceMesh.FaceMesh(static_image_mode=self.staticMode,
                                                 max_num_faces=self.maxFaces,
                                                 min_detection_confidence=self.minDetectionCon,
                                                 min_tracking_confidence=self.minTrackCon,
                                                 refine_landmarks=self.landmark)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

    def findFaceMesh(self, img, draw=True):
       
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                               self.drawSpec, self.drawSpec)
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    img_height, img_width, img_channel = img.shape
                    x, y = int(lm.x * img_width), int(lm.y * img_height)
                    face.append([x, y])
                faces.append(face)
        return img, faces, self.results

    def findDistance(self,point1, point2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = point1
        x2, y2 = point2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 1, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 1, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
            # cv2.circle(img, (cx, cy), 1, (255, 0, 255), cv2.FILLED)
            return length,info, img
        else:
            return length, info


def main():
    cap = cv2.VideoCapture(0)


    detector = GetFaceMesh(staticMode=False, maxFaces=1, minDetectionCon=0.5, minTrackCon=0.5)

   
    while True:
       
        success, img = cap.read()

        
        img, faces = detector.findFaceMesh(img, draw=True)

        
        if faces:
           
            for face in faces:
                
                leftEyeUpPoint = face[159]
                leftEyeDownPoint = face[23]
                
                leftEyeVerticalDistance, info = detector.findDistance(leftEyeUpPoint, leftEyeDownPoint)

                print(leftEyeVerticalDistance)

        cv2.imshow("Image", img)

        cv2.waitKey(1)


if __name__ == "__main__":
    main()
