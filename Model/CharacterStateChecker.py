import cv2 as cv
import numpy as np

from threading import Lock

from ColorSegmentator import ColorSegmentator

segmentator = ColorSegmentator()

class CharacterStateChecker:
    
    def __init__(self, need_to_heal:bool=None, can_e_attack:bool=None) -> None:
        self.need_to_heal = need_to_heal
        self.can_e_attack = can_e_attack

    def update_need_to_heal_flag(self, need_to_heal: bool) -> None:
        self.need_to_heal = need_to_heal

    def update_can_e_attack_flag(self, can_e_attack: bool) -> None:
        self.can_e_attack = can_e_attack

    @property
    def serialized(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

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