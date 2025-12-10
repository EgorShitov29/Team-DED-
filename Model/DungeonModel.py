from detection.Detector import Detector
from Aimer import Aimer
from EnemyAimer import EnemyAimer
from BattleStrategy import BattleStrategy
from EntertToDungeon import enter_to_dungeon
from ScreenCapture import ScreenCapture, BattleScreenCapture
from ConfirmSquadBuild import ConfirmSquadLevel
from ColorSegmentator import ColorSegmentator
from FrameTextCoordinator import FrameTextCoordinator
from EntertToDungeon import enter_to_dungeon
from ActivateDungeon import activate_dungeon

import time
import cv2 as cv
import numpy as np
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from typing import Optional


class DungeonModel:

    def __init__(self):
        self.detector_enemy = Detector('detection/weights/enemy_best.pt')
        self.detector_tree = Detector('detection/weights/tree_best.pt')
        self.enemy_aimer = EnemyAimer(screen_center=(1920, 1080))
        self.tree_aimer = Aimer(screen_size=(1920, 1080))
        self.level_salector = LevelSelector()
        self.text_coordinator = FrameTextCoordinator()
        self.confirm_squad_level = ConfirmSquadLevel()
        self.battle = BattleStrategy()

    def enter(self, frame, event_type='invite'):
        return enter_to_dungeon(frame, event_type)

    def activate(self, event_type='activate'):
        result = activate_dungeon()
        return result

