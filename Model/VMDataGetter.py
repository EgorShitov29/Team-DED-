import cv2 as cv


class DataGetter:

    def __init__(self, dungeon_level: int, frame: cv.typing.MatLike):
        self.dungeon_level = dungeon_level
        self.frame = frame
    
    def get_data(self) -> dict:
        return {'dungeon_level': self.dungeon_level,
                'frame': self.frame}