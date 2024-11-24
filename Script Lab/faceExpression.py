from deepface import DeepFace
import asyncio 

class FaceExpression:

    def __init__(self,enforce_detection = False, detector_backend = "opencv",align = False):
        self.enforce_detection = enforce_detection
        self.detector_backend = detector_backend
        self.detector_backend_list = ['opencv','dlib','mediapipe']
        self.align = align

    def getFaceExpression(self,image) -> dict :
        analysisResult = DeepFace.analyze(image,
                                          #action list goes here 
                                          enforce_detection= self.enforce_detection,
                                          detector_backend=self.detector_backend_list[0],
                                          align=self.align
                                          )

        emotiondict = analysisResult[0]["emotion"]
        dominantemotion = analysisResult[0]["dominant_emotion"]
        face_confidence = analysisResult[0]['face_confidence']
        age = analysisResult[0]['age']
        dominant_gender = analysisResult[0]['dominant_gender']
        left_eye_region = analysisResult[0]['region']['left_eye']
        right_eye_region = analysisResult[0]['region']['right_eye']

        analysisDict = { 
            "emotiondict":emotiondict,
            "dominantemotion":dominantemotion,
            "face_confidence":face_confidence,
            "age":age,
            "dominant_gender":dominant_gender,
            "leye_region":left_eye_region,
            "reye_region":right_eye_region
        }

        return analysisDict

