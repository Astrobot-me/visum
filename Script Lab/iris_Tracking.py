import cv2
import mediapipe as mp


import numpy as np
import time
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Initialize Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

# Eye and Iris landmarks for left and right eyesq
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# To store iris movement data
history_length = 50
left_eye_horizontal = deque(maxlen=history_length)
left_eye_vertical = deque(maxlen=history_length)
right_eye_horizontal = deque(maxlen=history_length)
right_eye_vertical = deque(maxlen=history_length)

def detect_iris_position(iris_landmarks, eye_landmarks):
    """
    Detect the horizontal and vertical position of the iris relative to the eye corners and bounds.
    """
    iris_center = np.mean(iris_landmarks, axis=0)  # Center of the iris
    left_corner = eye_landmarks[0]
    right_corner = eye_landmarks[3]
    top_corner = eye_landmarks[1]
    bottom_corner = eye_landmarks[5]

    # Calculate ratios
    eye_width = np.linalg.norm(right_corner - left_corner)
    eye_height = np.linalg.norm(top_corner - bottom_corner)
    horizontal_ratio = (iris_center[0] - left_corner[0]) / eye_width
    vertical_ratio = (iris_center[1] - top_corner[1]) / eye_height

    # Determine direction based on the ratios
    horizontal_direction = "Center"
    vertical_direction = "Center"

    if horizontal_ratio < 0.35:
        horizontal_direction = "Left"
    elif horizontal_ratio > 0.65:
        horizontal_direction = "Right"

    if vertical_ratio < 0.35:
        vertical_direction = "Up"
    elif vertical_ratio > 0.65:
        vertical_direction = "Down"

    return horizontal_ratio, vertical_ratio, horizontal_direction, vertical_direction

# Initialize video capture and FPS calculation
cap = cv2.VideoCapture(0)
prev_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    # Get frame dimensions
    height, width, _ = frame.shape

    # Create black sidebars for displaying text and graph
    sidebar_width = 300
    left_sidebar = np.zeros((height, sidebar_width, 3), dtype=np.uint8)  # Left Sidebar for direction
    right_sidebar = np.zeros((height, sidebar_width, 3), dtype=np.uint8)  # Right Sidebar for ratio

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Extract landmarks
            landmarks = np.array([[lm.x * width, lm.y * height] for lm in face_landmarks.landmark])
            
            left_eye = landmarks[LEFT_EYE]
            right_eye = landmarks[RIGHT_EYE]
            left_iris = landmarks[LEFT_IRIS]
            right_iris = landmarks[RIGHT_IRIS]

            # Detect Iris Positions (both ratios and directions)
            left_horizontal, left_vertical, left_horizontal_direction, left_vertical_direction = detect_iris_position(left_iris, left_eye)
            right_horizontal, right_vertical, right_horizontal_direction, right_vertical_direction = detect_iris_position(right_iris, right_eye)

            # Append to history
            left_eye_horizontal.append(left_horizontal)
            left_eye_vertical.append(left_vertical)
            right_eye_horizontal.append(right_horizontal)
            right_eye_vertical.append(right_vertical)

            # Draw eyes and iris for visualization
            for point in LEFT_EYE + RIGHT_EYE + LEFT_IRIS + RIGHT_IRIS:
                cv2.circle(frame, (int(landmarks[point][0]), int(landmarks[point][1])), 2, (255, 0, 0), -1)  # Blue Circles

            # Display directional movements (left, right, up, down) on the left sidebar
            cv2.putText(left_sidebar, "Iris Direction", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(left_sidebar, f"Left Eye: {left_horizontal_direction}, {left_vertical_direction}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(left_sidebar, f"Right Eye: {right_horizontal_direction}, {right_vertical_direction}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Display horizontal and vertical ratios on the right sidebar
            cv2.putText(right_sidebar, "Iris Movement Ratios", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(right_sidebar, f"Left Eye: H={left_horizontal:.2f}, V={left_vertical:.2f}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(right_sidebar, f"Right Eye: H={right_horizontal:.2f}, V={right_vertical:.2f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Create a graph with matplotlib
    fig = Figure(figsize=(3, 2), dpi=100)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.plot(left_eye_horizontal, label="Left Eye H", color="blue")
    ax.plot(left_eye_vertical, label="Left Eye V", color="cyan")
    ax.plot(right_eye_horizontal, label="Right Eye H", color="green")
    ax.plot(right_eye_vertical, label="Right Eye V", color="magenta")
    ax.legend(loc="upper right")
    ax.set_title("Iris Movement")
    ax.set_ylim(0, 1)  # Normalize for ratio values
    ax.grid()

    # Convert matplotlib plot to image
    canvas.draw()
    graph_image = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    graph_image = graph_image.reshape(canvas.get_width_height()[::-1] + (3,))
    graph_image = cv2.cvtColor(graph_image, cv2.COLOR_RGB2BGR)

    # Resize graph to fit the sidebar
    graph_image = cv2.resize(graph_image, (sidebar_width, int(height / 2)))

    # Place the graph on the right sidebar
    right_sidebar[-graph_image.shape[0]:, :, :] = graph_image

    # Combine the camera feed and sidebars
    combined_frame = np.hstack((left_sidebar, frame, right_sidebar))

    # Show the combined frame
    cv2.imshow("Iris Movement Tracking", combined_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
