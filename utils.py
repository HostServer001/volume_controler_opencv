import math
import numpy as np
from cv2.typing import MatLike
from typing import Optional

class Supervisor:
    """A class to supervise and record hand landmark positions and distances."""
    def __init__(self):
        self.record_array = np.array([(0,0)])
        self.dist_record_array = [0]
        self.is_controler = False

    def _append(self, arr_1, arr_2)->MatLike:
        """Appends two arrays vertically. For internal use only"""
        arr_2 = np.array(arr_2).reshape(1, 2)
        return np.concatenate((arr_1, arr_2), axis=0)

    def supervise(self, x, y)->None:
        """Records the (x,y) position of a specific landmark if it has changed."""
        to_compare = tuple(self.record_array[-1])
        if (x, y) == to_compare:
            pass
        else:
            self.record_array = self._append(self.record_array, [(x, y)])        
    
    def dist_supervise(self,dist:int,*args,**kwargs)->None:
        """Records the distance between two landmarks if it has changed. Also calls main() if is_controler is True."""
        """param
        dist: Distance between two landmarks
        """
        # if dist == self.dist_record_array[-1]:
        #     pass
        # else:
        #     self.dist_record_array.append(dist)
        self.dist_record_array.append(dist)
        if self.is_controler:
            self.main(*args,**kwargs) # type: ignore

def count_fingers(landmarks)->int:
    """Count the number of fingers raised based on landmarks."""
    count = 0
    FINGER_TIPS = [8, 12, 16, 20]
    THUMB_TIP = 4
    for tip in FINGER_TIPS:
        if landmarks[tip][1] < landmarks[tip - 2][1]:
            count += 1
    if landmarks[THUMB_TIP][0] > landmarks[THUMB_TIP - 1][0]:
        count += 1
    return count

def get_index(pos_name:str)->Optional[int]:
    """Returns the index of the hand landmark based on its name. Check hand_ref_img.png for reference."""
    """param 
    pos_name: Name of the landmark as a string
    """
    hand_landmarks = {
    "WRIST": 0,
    "THUMB_CMC": 1,
    "THUMB_MCP": 2,
    "THUMB_IP": 3,
    "THUMB_TIP": 4,
    "INDEX_FINGER_MCP": 5,
    "INDEX_FINGER_PIP": 6,
    "INDEX_FINGER_DIP": 7,
    "INDEX_FINGER_TIP": 8,
    "MIDDLE_FINGER_MCP": 9,
    "MIDDLE_FINGER_PIP": 10,
    "MIDDLE_FINGER_DIP": 11,
    "MIDDLE_FINGER_TIP": 12,
    "RING_FINGER_MCP": 13,
    "RING_FINGER_PIP": 14,
    "RING_FINGER_DIP": 15,
    "RING_FINGER_TIP": 16,
    "PINKY_MCP": 17,
    "PINKY_PIP": 18,
    "PINKY_DIP": 19,
    "PINKY_TIP": 20
    }

    if pos_name:
        for i in hand_landmarks.keys():
            if pos_name == i:
                return hand_landmarks[i]
    
def round_of(num:int,round_of_to:int=10)->int:
    """Rounds a numebr to nearest round_of_to default 10"""
    """param
    num: Number to be rounded
    round_of_to: Number to round of to default 10
    """
    rounded = round(num/round_of_to)*round_of_to
    return int(rounded)

def get_distance(landmarks,finger1_lm:str,finger2_lm:str)->int:
    """Calculates the distance bw two finger landmarsks"""
    """param
    landmarks: List of landmarks
    finger1_lm: Name of first landmark as string
    finger2_lm: Name of second landmark as string"""
    x_1,y_1 = landmarks[get_index(pos_name = finger1_lm)][0],landmarks[get_index(pos_name = finger1_lm)][1]
    x_1,y_1 = round_of(x_1),round_of(y_1)

    x_2,y_2 = landmarks[get_index(pos_name = finger2_lm)][0],landmarks[get_index(pos_name = finger2_lm)][1]
    x_2,y_2 = round_of(x_2),round_of(y_2)

    return int(math.sqrt(((x_1-x_2)**2)+((y_1-y_2)**2)))

