from concurrent.futures import ThreadPoolExecutor
from typing import Optional, List, Tuple

import time


class CollectItemsStrategy:
    """
    Стратегия сбора предметов после боя.
    Предполагается, что снаружи передаётся:
    - grab_frame: callable -> np.ndarray (скрин)
    - detect_items: callable(frame) -> List[bbox]
    - mover: объект с методами move_to(x, y) и interact()
    """

    def __init__(
        self,
        grab_frame,
        detect_items,
        mover,
        screen_size: Tuple[int, int],
        max_workers: int = 2,
        collect_timeout: float = 15.0,
    ) -> None:
        self.grab_frame = grab_frame
        self.detect_items = detect_items
        self.mover = mover
        self.screen_w, self.screen_h = screen_size
        self.pool_executor = ThreadPoolExecutor(max_workers=max_workers)
        self.collect_timeout = collect_timeout

    def _center_of_bbox(self, bbox) -> Tuple[int, int]:
        """
        bbox: (x1, y1, x2, y2) либо dict с такими полями.
        """
        if isinstance(bbox, dict):
            x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
        else:
            x1, y1, x2, y2 = bbox
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        return cx, cy

    def _pick_closest(self, bboxes: List) -> Optional:
        if not bboxes:
            return None
        cx_screen = self.screen_w // 2
        cy_screen = self.screen_h // 2

        def dist2(b):
            x, y = self._center_of_bbox(b)
            dx = x - cx_screen
            dy = y - cy_screen
            return dx * dx + dy * dy

        return min(bboxes, key=dist2)

    def run_once(self) -> bool:
        """
        Один шаг: получить кадр, найти предметы, подойти к ближайшему и поднять.
        Возвращает True, если что-то попытались собрать.
        """
        frame = self.grab_frame()
        bboxes = self.detect_items(frame)
        if not bboxes:
            return False

        target = self._pick_closest(bboxes)
        if target is None:
            return False

        tx, ty = self._center_of_bbox(target)

        # Двигаемся к цели и жмём interact
        self.mover.move_to(tx, ty)
        time.sleep(0.3)
        self.mover.interact()
        return True

    def run_loop(self) -> None:
        """
        Цикл сбора до истечения таймера или пока предметы не закончились несколько итераций подряд.
        """
        start = time.time()
        empty_iterations = 0
        while time.time() - start < self.collect_timeout:
            collected = self.run_once()
            if not collected:
                empty_iterations += 1
                if empty_iterations >= 3:
                    break
                time.sleep(0.5)
            else:
                empty_iterations = 0
                time.sleep(0.2)
