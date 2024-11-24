import cv2
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Face Mesh model
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define camera matrix and distortion coefficients (assuming no lens distortion)
frame_width, frame_height = 640, 480  # Adjust according to your webcam resolution
focal_length = frame_width
cam_matrix = np.array([[focal_length, 0, frame_width / 2],
                       [0, focal_length, frame_height / 2],
                       [0, 0, 1]])
dist_coeffs = np.zeros((4, 1))

# Define 3D model points (based on a generic head model)
model_points = np.array([
    [0.0, 0.0, 0.0],          # Nose tip (landmark 1)
    [0.0, -63.6, -12.0],      # Chin (landmark 152)
    [-43.3, 32.7, -26.0],     # Left eye left corner (landmark 263)
    [43.3, 32.7, -26.0],      # Right eye right corner (landmark 33)
    [-28.9, -28.9, -24.1],    # Left Mouth corner (landmark 61)
    [28.9, -28.9, -24.1]      # Right Mouth corner (landmark 291)
], dtype=np.float64)

# Define the corresponding 2D points
def get_2d_landmarks(landmarks, img_width, img_height):
    """
    Extract relevant 2D points for head pose estimation.
    """
    return np.array([
        [landmarks[1].x * img_width, landmarks[1].y * img_height],   # Nose tip
        [landmarks[152].x * img_width, landmarks[152].y * img_height],  # Chin
        [landmarks[263].x * img_width, landmarks[263].y * img_height],  # Left eye left corner
        [landmarks[33].x * img_width, landmarks[33].y * img_height],   # Right eye right corner
        [landmarks[61].x * img_width, landmarks[61].y * img_height],   # Left Mouth corner
        [landmarks[291].x * img_width, landmarks[291].y * img_height]  # Right Mouth corner
    ], dtype=np.float64)

# Function to estimate the head pose
def estimate_head_pose(image, landmarks):
    image_height, image_width, _ = image.shape

    # Get 2D image points from the landmarks
    image_points = get_2d_landmarks(landmarks, image_width, image_height)

    # Use solvePnP to estimate the head pose
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, cam_matrix, dist_coeffs
    )

    if not success:
        return None, None, None

    # Project a 3D axis onto the image plane
    axis = np.float32([[100, 0, 0], [0, 100, 0], [0, 0, 100]])
    imgpts, _ = cv2.projectPoints(axis, rotation_vector, translation_vector, cam_matrix, dist_coeffs)

    # Check if we have all the projected points
    if imgpts is None or len(imgpts) != 3:
        return rotation_vector, translation_vector, None

    return rotation_vector, translation_vector, imgpts

# Main function to capture video and perform head pose estimation
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (frame_width, frame_height))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Face Mesh
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            rotation_vector, translation_vector, imgpts = estimate_head_pose(frame, face_landmarks.landmark)

            if imgpts is not None:
                # Draw the axes on the image
                nose_point = (int(imgpts[0][0][0]), int(imgpts[0][0][1]))
                
                # Ensure that all imgpts are available before drawing
                if len(imgpts) >= 3:
                    cv2.line(frame, nose_point, (int(imgpts[0][0][0]), int(imgpts[0][0][1])), (0, 0, 255), 3)  # X-axis (red)
                    cv2.line(frame, nose_point, (int(imgpts[1][0][0]), int(imgpts[1][0][1])), (0, 255, 0), 3)  # Y-axis (green)
                    cv2.line(frame, nose_point, (int(imgpts[2][0][0]), int(imgpts[2][0][1])), (255, 0, 0), 3)  # Z-axis (blue)

    cv2.imshow('Head Pose Estimation', frame)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
