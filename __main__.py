import cv2
import gestures
from utils import *
import mediapipe as mp
from cv2.typing import MatLike

# Initialize Mediapipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# Define finger tips landmarks
FINGER_TIPS = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
THUMB_TIP = 4

# Initialize Video Capture
cap = cv2.VideoCapture(0)

# Initialize Volume Controller
vol_dist_supervisor = gestures.VolumeControler()

def process_frame(frame)->MatLike:
    """Process a single video frame to detect hand landmarks and perform actions."""
    # Flip and convert frame to RGB
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    finger_count = 0
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            landmarks = extract_landmarks(hand, frame.shape)
            finger_count = count_fingers(landmarks)
            apply_rules(landmarks,frame)
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    # Display finger count on the frame
    cv2.putText(frame, f'Fingers: {finger_count}', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    return frame

def extract_landmarks(hand, frame_shape)->list:
    """Extract and round hand landmarks from Mediapipe results."""
    h, w, _ = frame_shape
    return [(round_of(lm.x * w), round_of(lm.y * h)) for lm in hand.landmark]

def apply_rules(landmarks,frame)->None:
    """Calculate and supervise the distance between index finger tip and thumb tip."""
    distance = get_distance(landmarks=landmarks, finger1_lm="INDEX_FINGER_TIP", finger2_lm="THUMB_TIP")
    distance = round_of(int(distance),20)
    vol_dist_supervisor.dist_supervise(distance,frame,landmarks)

def main()->None:
    """Main function to run the hand tracking application."""
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        frame = process_frame(frame)

        # Show the processed frame
        cv2.imshow("Hand Tracker", frame)

        # Exit on ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            print(vol_dist_supervisor.dist_record_array)
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
