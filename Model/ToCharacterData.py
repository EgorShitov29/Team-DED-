import cv2 as cv 
import numpy as np

from utils.frame_editors import frame_cropper


class ToCharacterData:

    def __init__(self, frame: cv.typing.MatLike) -> None:
        self._frame = frame

    def __get_life_bar_window(self) -> cv.typing.MatLike:
        cropped_img = frame_cropper(frame=self.frame, crop_percent=0.1, to_x1=3, to_x2=3, to_y1=0.8, to_y2=0.3)
        return cropped_img

    def __get_e_active_window(self) -> cv.typing.MatLike:
        height, width = self.frame.shape[:2]
        right_x = round(width * 0.91)
        bottom_y = round(height * 0.97)
        window_width = round(width * 0.05)
        window_height = round(height * 0.1)
        x1 = right_x - window_width
        y1 = bottom_y - window_height
        x2 = right_x
        y2 = bottom_y
        e_window = self.frame[y1:y2, x1:x2]
        return e_window

    def get_windows()