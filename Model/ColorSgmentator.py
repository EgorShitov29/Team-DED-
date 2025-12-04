import cv2 as cv
import numpy as np

from .hsv_borders import hsv_borders

class ColorSegmentator:

    def __init__(self, hsv_borders: dict=hsv_borders):
        self.hsv_borders = hsv_borders

    def create_mask(self, frame, color) -> cv.typing.MatLike:
        lower = self.hsv_borders[color]['lower']
        upper = self.hsv_borders[color]['upper']
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower, upper)
        return mask

    def count_non_zero_pixels(self, mask) -> int:
        return cv.countNonZero(mask)

if __name__ == '__main__':
    cs = ColorSegmentator()
    image = cv.imread('/home/kali/dev/genshin/photo/screen_port_135.png')

    height, width = image.shape[:2]

    bottom_y = height
    window_widht = round(width * 0.1)
    window_height = round(height * 0.1)
    center_x = width // 2
    x1 = center_x - window_widht 
    y1 = bottom_y - window_height
    x2 = center_x + window_widht 
    y2 = bottom_y + window_height
    cropped_img = image[y1:y2, x1:x2]

    mask = cs.create_mask(cropped_img, 'salad_green')
    cv.imshow('mask', mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    print(cs.count_non_zero_pixels(mask))