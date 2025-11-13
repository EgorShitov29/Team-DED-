import cv2 as cv
import numpy as np

import os


def frame_cropper(frame: cv.typing.MatLike, crop_percent: float, to_x1: int|float, to_x2: int|float, to_y1: int|float, to_y2: int|float) -> cv.typing.MatLike:
    """
    Функция обрезает изображение по заданным параметрам
    """
    height, width = frame.shape[:2]
    bottom_y = height
    window_widht = round(width * crop_percent)
    window_height = round(height * crop_percent)
    center_x = width // 2
    x1 = center_x - window_widht // to_x1
    y1 = bottom_y - int(window_height * to_y1)
    x2 = center_x + window_widht // to_x2
    y2 = bottom_y - int(window_height * to_y2)
    cropped_img = frame[y1:y2, x1:x2]
    return cropped_img