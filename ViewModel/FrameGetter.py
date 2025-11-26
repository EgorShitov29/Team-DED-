import cv2 as cv
import pyautogui as pgui
import numpy as np


class FrameGetter:

    def __init__(self):
        pass

    def get_frame(self) -> cv.typing.MatLike:
        screenshot = pgui.screenshot()
        to_np = np.array(screenshot)
        return cv.cvtColor(to_np, cv.COLOR_RGB2BGR)

if __name__ == '__main__':
    fg = FrameGetter()
    sc = fg.take_screenshot()
    cv.imshow('sc', sc)
    cv.waitKey(0)
    cv.destroyAllWindows()