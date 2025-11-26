import cv2 as cv
import numpy as np
import easyocr

import os

from utils.frame_editors import frame_cropper


class CharacterStateChecker:
    
    def __init__(self, frame: cv.typing.MatLike, reader: easyocr.Reader):
        self.frame = frame

    def character_life_check(self) -> tuple[int, int]:
        cropped_img = None
        remain, full = int(reader.readtext(cv.cvtColor(cropped_img, cv.COLOR_BGR2GRAY))[0][1].split('/')[0]), int(reader.readtext(cv.cvtColor(cropped_img, cv.COLOR_BGR2GRAY))[0][1].split('/')[-1])
        return (full, remain)

    def e_attack_state_check(self):
        pass

    def ultimate_attack_state_check(self):
        pass