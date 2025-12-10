import cv2 as cv
import pyautogui as pgui

import state_check.src.search_text_frame as text_opp
import gameplay_core as core


class LevelSelector:
    
    def __init__(self, target_squad_level: int=81) -> None:
        self.target_squad_level = target_squad_level

    def _find_squad_level(self, text: str) -> None | int:
        """
        Функция ищет уровень отряда по паттерну
        Возвращает результат поиска: пустое значение либо число
        """
        pattern = r'ур\. отряда:\s*(\d+)'
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
        return match

    def _find_closest(self, numbers, target):
        return min(numbers, key=lambda x: abs(x - target))

    def _find_levels(self, text_and_coords: dict):
        num_coords = dict()
        for text in text_and_coords.keys():
            match = self._find_squad_level(text)
            if match:
                num_coords[match] = text_and_coords[text]
        return num_coords

    def select_level(self, text_and_coords: dict):
        num_coords = self._find_levels(text_and_coords)
        closest = self._find_closest(num_coords.keys(), self.target_squad_level)
        bbox = num_coords[closest]
        centerx = (bbox[2] - bbox[0]) // 2
        centery = (bbox[3] - bbox[1]) // 2
        pgui.moveTo(x=centerx, y=centery)
        pgui.click()
        return True