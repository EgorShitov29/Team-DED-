import cv2 as cv 
import numpy as np


class ToCharacterData:
    def __init__(self, crop_percent=0.1, to_x1=2, to_y1=1.0, to_x2=2, to_y2=0.0):
        self.crop_percent = crop_percent
        self.to_x1 = to_x1
        self.to_y1 = to_y1
        self.to_x2 = to_x2
        self.to_y2 = to_y2

    def __get_life_bar_window(self, frame) -> cv.typing.MatLike:
        height, width = frame.shape[:2]
        bottom_y = height
        window_widht = round(width * self.crop_percent)
        window_height = round(height * self.crop_percent)
        center_x = width // 2
        x1 = center_x - window_widht // self.to_x1
        y1 = bottom_y - int(window_height * self.to_y1)
        x2 = center_x + window_widht // self.to_x2
        y2 = bottom_y - int(window_height * self.to_y2)
        return frame[y1:y2, x1:x2]

    def __get_e_active_window(self, frame) -> cv.typing.MatLike:
        height, width = frame.shape[:2]
        right_x = round(width * 0.91)
        bottom_y = round(height * 0.97)
        window_width = round(width * 0.05)
        window_height = round(height * 0.1)
        x1 = right_x - window_width
        y1 = bottom_y - window_height
        x2 = right_x
        y2 = bottom_y
        e_window = frame[y1:y2, x1:x2]
        return e_window

    def get_windows(self, frame) -> dict:
        window_data = dict()
        window_data['heal'] = self.__get_life_bar_window(frame)
        window_data['e'] = self.__get_e_active_window(frame)
        return window_data