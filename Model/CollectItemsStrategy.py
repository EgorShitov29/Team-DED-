import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np
from typing import Optional

from detection.Detector import Detector
from Aimer import Aimer
import gameplay_core as core
from ScreenCapture import ScreenCapture
from CharacterStateChecker import need_to_heal, can_e_attack


class MoveToTree:

    def __init__(self, detector: Detector, aimer: Aimer):
        self.detector = detector
        self.aimer = aimer
        self.frame_getter = ScreenCapture()
        self.frame_queue = Queue(maxsize=2)
        self.detection_queue = Queue(maxsize=2)
        self._is_running = False

    def start(self):
        self._is_running = True
        self.frame_getter.start()
        detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        detection_thread.start()

    def stop(self):
        self._is_running = False
        self.pool_executor.shutdown(wait=True)

    def _detection_loop(self):
        while self._is_running:
            frame_data = self.frame_getter.get_frame_data()
            if frame_data and frame_data['frame'] is not None:
                future = self.pool_executor.submit(self.detector.detect, frame_data['frame'])
                detection_data = future.result(timeout=0.1)
                sefl.detection_queue.put(detection_data, timeout=0.01)

    def _execute_game_command(self, command: Optional[str]):
        """
        Возможно, будет лучше сделать словарь с командами, но, как мне кажется - это лишнее. Пока так
        """
        if command == 'activate':
            core.click_event()
        elif len(command) == 2:
            core.hold_hotkey(command)
        elif len(command) == 1:
            core.hold_key(command)

    def process_frame(self):
        try:
            frame_data = self.frame_getter.get_frame_data()
            if not frame_data:
                return False
            detection_data = self.detection_queue.get_nowait()
        except:
            frame_data = self.frame_getter.get_frame_data()
            if not frame_data:
                return False
        command = self.aimer.get_aim_command(detection_data)
        self._execute_game_command(command)
        return True


class CollectItems:
    """
    Попробуйте применить поиск шаблонов
    и FrameTextCoordinator, чтобы определить,
    сколько осталось смолы
    """