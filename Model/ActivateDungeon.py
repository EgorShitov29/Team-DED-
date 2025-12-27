from typing import Optional, Tuple

import cv2 as cv
import numpy as np

from Model.FrameTextCoordinator import FrameTextCoordinator


class ActivateDungeon:
    """
    Открытие окна старта подземелья и нажатие кнопки "Начать".
    """

    def __init__(self, grab_frame, frame_text: FrameTextCoordinator, clicker) -> None:
        self.grab_frame = grab_frame
        self.frame_text = frame_text
        self.clicker = clicker  # объект с методом click(x, y)

    def _find_start_button(self, frame) -> Optional[Tuple[int, int, int, int]]:
        """
        Использует OCR через FrameTextCoordinator, чтобы найти кнопку "Начать".
        При необходимости текст/язык можно вынести в конфиг.
        """
        res = self.frame_text.get_text_and_coords(frame, "Начать")
        if res is None:
            # можно добавить fallback: искать по английскому "Start"
            res = self.frame_text.get_text_and_coords(frame, "Start")
        if res is None:
            return None
        _, bbox = res
        return bbox

    def open_start_menu(self) -> None:
        """
        При необходимости можно добавить логику открытия меню старта,
        если оно не появляется автоматически.
        """
        # пока заглушка, оставлена для совместимости с Orchestrator
        pass

    def press_start_if_visible(self) -> bool:
        frame = self.grab_frame()
        bbox = self._find_start_button(frame)
        if bbox is None:
            return False

        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        self.clicker.click(cx, cy)
        return True
