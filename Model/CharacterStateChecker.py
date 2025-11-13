import cv2 as cv
import numpy as np
import easyocr

import os

from utils.frame_editors import frame_cropper


class CharacterStateChecker:
    
    def __init__(self, frame: cv.typing.MatLike, reader: easyocr.Reader):
        self.frame = frame

    def __get_life_bar(self) -> cv.typing.MatLike:
        cropped_img = frame_cropper(frame=self.frame, crop_percent=0.1, to_x1=3, to_x2=3, to_y1=0.8, to_y2=0.3)
        return cropped_img

    def character_life_check(self) -> tuple[int, int]:
        cropped_img = self.__get_life_bar()
        remain, full = int(reader.readtext(cv.cvtColor(cropped_img, cv.COLOR_BGR2GRAY))[0][1].split('/')[0]), int(reader.readtext(cv.cvtColor(cropped_img, cv.COLOR_BGR2GRAY))[0][1].split('/')[-1])
        return (full, remain)

    def e_attack_state_check(self):
        pass

    def ultimate_attack_state_check(self):
        pass