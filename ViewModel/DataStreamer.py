import cv2 as cv
import numpy as np


class DataStreamer:

    def __init__(self, frame: cv.typing.MatLike=None, dungeon_level: int=None) -> None:
        self.dungeon_level = dungeon_level
        self._frame = frame
    
    @property
    def frame(self) -> cv.typing.MatLike:
        return self._frame

    @frame.setter
    def frame(self, new_frame) -> None:
        if not isinstance(new_frame, cv.typing.MatLike):
            raise 'У тебя ничего не получилось'
        self._frame = new_frame
