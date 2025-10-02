import os
import re
import cv2
import math
import subprocess
from utils import *

class VolumeControler(Supervisor):
    """A class to control system volume based on hand gestures. Inherits from Supervisor."""
    def __init__(self):
        super().__init__()
        self.is_controler = True
        self.max_finger_dist = 220 #default

    def get_vol(self)->Optional[int]:
        """Gets the current system volume percentage."""
        output = subprocess.run(["amixer", "get", "Master"], capture_output=True, text=True)
        match = re.search(r'\[(\d+)%\]', output.stdout)
        if match:
            return int(match.group(1))
        else:
            return 10 #remoove this later
    
    def increase_vol(self)->None:
        """Increases the system volume by 5%."""
        os.system("pactl set-sink-volume @DEFAULT_SINK@ +5%")
    
    def decrease_vol(self)->None:
        """Decreases the system volume by 5%."""
        os.system("pactl set-sink-volume @DEFAULT_SINK@ -5%")
    
    def set_vol(self,x:int)->None :
        """Set the system volume to x"""
        os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {x}%")
    
    def _set_prediction(self,landmarks)->None:
        """Get the hand prediction of max finger distance""" #unoptimized function right now
        diagonal_1 =  get_distance(
            landmarks = landmarks,
            finger1_lm = "THUMB_TIP",
            finger2_lm = "PINKY_TIP"
            )
        #try taking avg of diag_1 and diag_2
        diagonal_2 =  get_distance(
            landmarks = landmarks,
            finger1_lm = "MIDDLE_FINGER_TIP",
            finger2_lm = "WRIST"
            )
        prediction = 220/320*diagonal_1
        self.max_finger_dist = prediction
    
    def main(self,frame,landmarks)->None:
        """Main function to adjust volume based on distance changes."""
        if len(self.dist_record_array) > 2:
            del self.dist_record_array[:1]
        #Register the current ratio if not good contorl achived
        if count_fingers(landmarks) == 5:
            self._set_prediction(landmarks)
        l1 = self.dist_record_array[0]
        l2 = self.dist_record_array[1]

        vol = int(self.get_vol()) # type: ignore
        self.set_vol(l2/self.max_finger_dist*100)
        cv2.putText(frame, f'Current vol: {vol}', (frame.shape[1] - 500, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        if vol > 100:   #kill switch for linux users
            os.system("pactl set-sink-volume @DEFAULT_SINK@ 100%")
        # if l2-l1 > 0:
        #     self.increase_vol()
        # if l2-l1 < 0:
        #     self.decrease_vol()