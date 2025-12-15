import cv2 as cv
import numpy as np

from threading import Lock

from Model.ColorSegmentator import ColorSegmentator

segmentator = ColorSegmentator()

def need_to_heal(frame, health_hsv_border='salad_green'):
    mask = segmentator.create_mask(frame=frame, color=health_hsv_border)
    if segmentator.count_non_zero_pixels(mask) > 10:
        return False
    else:
        return True

def can_e_attack(frame, e_hsv_border='grey_e'):
    mask = segmentator.create_mask(frame=frame, color=e_hsv_border)
    if segmentator.count_non_zero_pixels(mask) > 10:
        return True
    else:
        return False