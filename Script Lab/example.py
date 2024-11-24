import cv2
import mediapipe as mp
import numpy as np
import time
import pygame  # For playing alert sound

# Initialize Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

# Mouth landmarks
UPPER_LIP = [13]
LOWER_LIP = [14]
LEFT_MOUTH_CORNER = [61]
RIGHT_MOUTH_CORNER = [291]

# Thresholds
YAWN_RATIO_UPPER_THRESHOLD = 0.6  # Upper limit for detecting a yawn
YAWN_RATIO_LOWER_THRESHOLD = 0.4  # Lower limit to reset the yawning state
ALERT_THRESHOLD = 3  # Number of yawns for an alert
ALERT_INTERVAL = 60  # Time interval in seconds
ALERT_SOUND_DURATION = 15  # Duration of alert sound in seconds

# Initialize variables
yawn_counter = 0
yawning = False
start_time = time.time()
alert_played = False  # To ensure alert is played only once per hazardous state
alert_start_time = None  # Time when alert sound starts playing

# Initialize pygame for sound playback
pygame.mixer.init()
alert_sound_path = "./sound.mp3"  # Update with the actual path to your sound file

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read() 
    if not ret:
        print("Failed to capture video. Exiting...")
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # Frame dimensions
    height, width, _ = frame.shape

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract the landmark coordinates
            landmarks = np.array([[lm.x * width, lm.y * height] for lm in face_landmarks.landmark])

            # Calculate mouth distances
            upper_lip = landmarks[UPPER_LIP[0]]
            lower_lip = landmarks[LOWER_LIP[0]]
            left_corner = landmarks[LEFT_MOUTH_CORNER[0]]
            right_corner = landmarks[RIGHT_MOUTH_CORNER[0]]

            vertical_distance = np.linalg.norm(upper_lip - lower_lip)
            horizontal_distance = np.linalg.norm(left_corner - right_corner)

            # Calculate the yawn ratio
            yawn_ratio = vertical_distance / horizontal_distance

            # Check if the person is yawning
            if yawn_ratio > YAWN_RATIO_UPPER_THRESHOLD:
                if not yawning:
                    yawning = True
                    yawn_counter += 1
            elif yawn_ratio < YAWN_RATIO_LOWER_THRESHOLD:
                yawning = False

            # Display the yawn ratio and counter
            cv2.putText(frame, f"Yawn Ratio: {yawn_ratio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Yawn Count: {yawn_counter}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Play alert sound only when yawn count reaches or exceeds 3
        if yawn_counter >= ALERT_THRESHOLD and not alert_played:
            try:
                pygame.mixer.music.load(alert_sound_path)
                pygame.mixer.music.play()
                alert_played = True  # Prevent replaying until reset
                alert_start_time = time.time()  # Record when the sound started
            except Exception as e:
                print(f"Failed to play sound: {e}")
        else:
            alert_played = False  # Reset alert state when yawn count is below threshold

    # Stop the alert sound after ALERT_SOUND_DURATION seconds
    if alert_played and alert_start_time:
        elapsed_alert_time = time.time() - alert_start_time
        if elapsed_alert_time >= ALERT_SOUND_DURATION:
            pygame.mixer.music.stop()  # Stop the alert sound after 15 seconds
            alert_played = False  # Reset alert played flag
            yawn_counter = 0  # Reset the yawn counter after the alert sound is triggered

    # Reset the timer and counter after ALERT_INTERVAL if sound hasn't been triggered
    elapsed_time = time.time() - start_time
    if elapsed_time >= ALERT_INTERVAL and not alert_played:
        start_time = time.time()
        yawn_counter = 0  # Reset the yawn count after 60 seconds if no alert
        alert_played = False  # Allow alert sound to trigger again after reset

    # Show the video frame
    cv2.imshow("Yawning Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
