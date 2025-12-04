import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np
from typing import Optional

from .detection.Detector import Detector
from .EnemyAimer import EnemyAimer
import .gameplay_core as core
from .ScreenCapture import ScreenCapture


class BattleStrategy:

    def __init__(self, detector: Detector, enemy_aimer: EnemyAimer):
        self.detector = detector
        self.enemy_aimer = enemy_aimer
        self.frame_getter = ScreenCapture()
        self.frame_queue = Queue(maxsize=2)
        self.detection_queue = Queue(maxsize=2)
        self.pool_executor = ThreadPoolExecutor(max_workers=2)
        self.stat = {
            'detected_enemies': 0,
            'curr_action': None
        }
        self._is_running = False

    def start(self):
        self._is_running = True
        self.frame_getter.start()
        threading.Thread(target=None, daemon=True).start()

    def stop(self):
        self._is_running = False
        self.pool_executor.shutdown(wait=True)

    def _detection_loop(self):
        while self._is_running:
            frame = self.frame_getter.get_frame()
            if frame is not None:
                detection_data = self.detector.detect(frame)
                sefl.detection_queue.put(detection_data, timeout=0.01)

    def _execute_game_command(self, command: Optional[str]):
        """
        Возможно, будет лучше сделать словарь с командами, но, как мне кажется - это лишнее. Пока так
        """
        if command == 'attack':
            core.attack_combination(4)
        elif len(command) == 2:
            core.hold_hotkey(command)
        elif len(command) == 1:
            core.hold_key(command)

     def process_frame(self) -> bool:
        try:
            detection_data = self.detection_queue.get_nowait()
        except:
            return False

        command = self.aimer.get_aim_command(detection_data)

        self._execute_game_command(command)

        self.stats['detected_enemies'] = len(detection_data)
        self.stats['curr_action'] = command or 'wait'