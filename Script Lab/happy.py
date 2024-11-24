import cv2
from deepface import DeepFace
from faceExpression import FaceExpression 
# Open a webcam to capture video
cap = cv2.VideoCapture(0)
faceexpression = FaceExpression()


while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Use DeepFace to analyze the image for emotions
    # result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

    # # Extract the dominant emotion from the result
    # emotion = result[0]['dominant_emotion']
    # print(f"Detected Emotion: {emotion}")

    emotiondict = faceexpression.getFaceExpression(frame)

    # Draw the emotion on the frame
    cv2.putText(frame, f"Emotion: {emotiondict['dominantemotion']} ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with the detected emotion
    cv2.imshow('Emotion Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close all windows
cap.release()
cv2.destroyAllWindows()
