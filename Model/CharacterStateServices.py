import cv2 as cv

from Model.ColorSegmentator import ColorSegmentator


class HealthService:
    def __init__(self, need_to_heal_border: int = 10):
        self.color_segmentator = ColorSegmentator()
        self.need_to_heal_border = need_to_heal_border

    def _get_bar_pixels(self, frame) -> int:
        mask = self.color_segmentator.create_mask(frame, 'salad_green')
        return self.color_segmentator.count_non_zero_pixels(mask)

    def get_heal_flag(self, frame) -> bool:
        pixels = self._get_bar_pixels(frame)
        return pixels > self.need_to_heal_border


def check_e_attack(frame_text: str) -> bool:
    if len(frame_text) > 1:
        return True
    else:
        return False