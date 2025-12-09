import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np
from typing import Optional

from detection.Detector import Detector
from EnemyAimer import EnemyAimer
import gameplay_core as core
from ScreenCapture import BattleScreenCapture
from CharacterStateChecker import need_to_heal, can_e_attack


class BattleStrategy:

    def __init__(self, detector: Detector, enemy_aimer: EnemyAimer):
        self.detector = detector
        self.enemy_aimer = enemy_aimer
        self.frame_getter = BattleScreenCapture()
        self.frame_queue = Queue(maxsize=2)
        self.detection_queue = Queue(maxsize=2)
        self.pool_executor = ThreadPoolExecutor(max_workers=2)
        self.stat = {
            'detected_enemies': 0,
            'need_to_heal': False,
            'can_e_attack': False,
            'curr_action': None
        }
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
        if command == 'attack':
            core.attack_combination(4)
        elif len(command) == 2:
            core.hold_hotkey(command)
        elif len(command) == 1:
            core.hold_key(command)

    def process_frame(self) -> bool:
        try:
            frame_data = self.frame_getter.get_frame_data()
            if not frame_data:
                return False
            detection_data = self.detection_queue.get_nowait()
        except:
            frame_data = self.frame_getter.get_frame_data()
            if not frame_data:
                return False

        need_to_heal = need_to_heal(frame_data['health_bar'])
        can_e_attack = can_e_attack(frame_datap['e_attack'])

        command = self.aimer.get_aim_command(detection_data)

        self._battle_logic(command, need_to_heal, can_e_attack)
        self.stats.update({
            'detected_enemies': len(detection_data),
            'need_to_heal': need_to_heal,
            'can_e_attack': can_e_attack,
            'curr_action': command or 'wait'
        })
        return True

    def _battle_logic(self, command, need_to_heal, can_e_attack):
        if need_to_heal:
            print('HEAL')
        
        if can_e_attack and len(self.stats['detected_enemies']) > 0:
            core.elemental_attack()

        self._execute_game_command(command)