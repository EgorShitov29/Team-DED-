import cv2 as cv


class DataGetter:

    def __init__(self, dungeon_level: int, frame: cv.typing.MatLike):
        self.dungeon_level = dungeon_level
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, new_frame: cv.typing.MatLike):
        self._frame = new_frame
    
    def get_data(self) -> dict:
        return {'dungeon_level': self.dungeon_level,
                'frame': self.frame}