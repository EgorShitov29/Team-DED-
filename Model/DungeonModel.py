from StateMachine import StateMachine
from detection.Detector import Detector
from Aimer import Aimer
from BattleStrategy import BattleStrategy
from EntertToDungeon import enter_to_dungeon
from ScreenCapture import ScreenCapture, BattleScreenCapture
from ConfirmSquadBuild import ConfirmSquadLevel
from ColorSegmentator import ColorSegmentator

import time
import cv2 as cv
import numpy as np
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from typing import Optional


class BotModel:

    def __init__(self):
        pass