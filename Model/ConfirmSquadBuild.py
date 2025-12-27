import time
import re
from typing import Optional, Tuple

from Model.FrameTextCoordinator import FrameTextCoordinator


class ConfirmSquadBuild:
    """
    Ожидание окна отряда и подтверждение состава.
    """

    def __init__(self, grab_frame, frame_text: FrameTextCoordinator, clicker, timeout: float = 10.0) -> None:
        self.grab_frame = grab_frame
        self.frame_text = frame_text
        self.clicker = clicker
        self.timeout = timeout

    def _find_confirm_button(self, frame) -> Optional[Tuple[int, int, int, int]]:
        """
        Ищет кнопку подтверждения (например, по тексту "Начать", "Готово", "Подтвердить").
        """
        for pattern in ["Начать", "Готово", "Подтвердить", "Start"]:
            res = self.frame_text.get_text_and_coords(frame, pattern)
            if res is not None:
                _, bbox = res
                return bbox
        return None

    def wait_and_confirm(self) -> bool:
        """
        Ждёт появления экрана отряда и жмёт кнопку подтверждения.
        Возвращает True при успехе.
        """
        start = time.time()
        while time.time() - start < self.timeout:
            frame = self.grab_frame()
            bbox = self._find_confirm_button(frame)
            if bbox is None:
                time.sleep(0.3)
                continue

            x1, y1, x2, y2 = bbox
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            self.clicker.click(cx, cy)
            return True

        return False
