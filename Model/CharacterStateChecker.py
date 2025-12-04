import cv2 as cv
import numpy as np

from threading import Lock

class CharacterStateChecker:
    
    def __init__(self, need_to_heal:bool=None, can_e_attack:bool=None) -> None:
        self.need_to_heal = need_to_heal
        self.can_e_attack = can_e_attack

    def update_need_to_heal_flag(self, need_to_heal: bool) -> None:
        self.need_to_heal = need_to_heal

    def update_can_e_attack_flag(self, can_e_attack: bool) -> None:
        self.can_e_attack = can_e_attack

    @property
    def serialized(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}