import cv2 as cv

from queue import Queue, Empty
import time

from .DataCollector import DataCollector
from .FrameTextCoordinator import FrameTextCoordinator
from .CharacterStateChecker import CharacterStateChecker
from .CharacterStateServices import HealthService, check_e_attack


class HealthCollector(DataCollector):
    
    def __init__(self, data_queue: Queue, health_service: HealthService, frame: cv.typing.MatLike=None) -> None:
        super().__init__(data_queue)
        self.health_service = health_service
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, new_frame):
        self._frame = new_frame

    def collect(self):
        while self.flag_running:
            flag_need_to_heal = self.health_service(self.frame)

            if health:
                self.data_queue.put(('need_to_heal', flag_need_to_heal))
                time.sleep(0.1)

class ElementalAttackCollector(DataCollector):
    
    def __init__(self, data_queue: Queue, ftcoordinator: FrameTextCoordinator, frame: cv.typing.MatLike=None) -> None:
        super().__init__(data_queue)
        self.ft = ftcoordinator
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, new_frame):
        self._frame = new_frame

    def collect(self):
        while self.flag_running:
            self.ftcoordinator.frame = self._frame
            e_attack = self.ftcoordinator.get_only_check()
            can_e_attack = check_e_attack(e_attack)

            if can_e_attack:
                self.data_queue.put(('can_e_attack', can_e_attack))


ft = FrameTextCoordinator()
if __name__ == '__main__':
    hc = HealthCollector(frame=cv.imread('../../photo/screen_port_78.png'), ftcoordinator=ft, data_queue=Queue())