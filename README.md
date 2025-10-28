Hand Gesture Volume Control (Linux - Debian Based)

This project is a hand gesture-based volume control system for Linux, built using Google’s MediaPipe and OpenCV. It detects your hand through the webcam, identifies landmarks, and adjusts the system volume based on the distance between your fingers — no need to touch your keyboard or mouse!


---

Features
Real-time hand tracking using Google’s MediaPipe Hands.

Simple rule-based logic to interpret gestures from hand landmark coordinate
 
Controls system volume dynamically for Debian-based Linux systems.

Lightweight — works smoothly on mid-range hardware.



---

Tech Stack

Python 3

OpenCV – for video capture and frame processing

MediaPipe – for hand detection and landmark extraction

---

Installation

1. Clone the repository

git clone https://github.com/HostServer001/volume_controler_opencv.git
cd volume_controler_opencv

2. Install dependencies

pip install opencv-python mediapipe

3. Run the program

python3 main.py


---

How It Works

1. MediaPipe detects the hand and provides 21 landmarks.


2. The code tracks the distance between thumb and index finger tips.


3. This distance is mapped to a volume percentage (0% → min distance, 100% → max distance).


4. Linux volume is adjusted using amixer or pactl commands.




---

🐧 Compatibility

✅ Debian-based Linux distributions only (e.g., Ubuntu, Pop!_OS, Kali Linux, etc.)

❌  Will not work on Windows and macOS



---

Limitations

Requires a working webcam.

Gesture detection accuracy depends on lighting and camera quality.

Not an “AI genius” solution — it’s a practical rule-based implementation using existing models.



--- 


License

This project is open-source and available under the MIT License.


---


Acknowledgements

Google MediaPipe for the hand tracking model.

OpenCV for computer vision utilities