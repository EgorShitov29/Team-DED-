from typing import List, Tuple, Optional

from .utils.enemy_position import bbox_centers

class EnemyAimer:
    """
    Выбор цели и выдача команды прицеливания/атаки.
    Ожидает, что bboxes врагов приходят в формате (x1, y1, x2, y2).
    """

    def __init__(self, screen_size: Tuple[int, int], mover, attacker, max_angle: float = 40.0) -> None:
        self.screen_w, self.screen_h = screen_size
        self.mover = mover
        self.attacker = attacker
        self.max_angle = max_angle

    def _screen_center(self) -> Tuple[int, int]:
        return self.screen_w // 2, self.screen_h // 2

    def select_target(self, enemy_bboxes: List[Tuple[int, int, int, int]]) -> Optional[Tuple[int, int, int, int]]:
        """
        Выбирает ближайшего к центру экрана врага.
        """
        if not enemy_bboxes:
            return None

        cx, cy = self._screen_center()
        centers = bbox_centers(enemy_bboxes)

        def dist2(c):
            dx = c[0] - cx
            dy = c[1] - cy
            return dx * dx + dy * dy

        best_idx = min(range(len(centers)), key=lambda i: dist2(centers[i]))
        return enemy_bboxes[best_idx]

    def is_attackable(self, bbox: Tuple[int, int, int, int]) -> bool:
        """
        Проверяет, не слишком ли далеко цель от центра экрана.
        Тут можно использовать простую метрику по пикселям.
        """
        if bbox is None:
            return False

        cx, cy = self._screen_center()
        tx, ty = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        dx = tx - cx
        dy = ty - cy
        dist = (dx * dx + dy * dy) ** 0.5

        # простая эвристика: если цель близко к центру — можно бить
        max_pixels = min(self.screen_w, self.screen_h) * 0.25
        return dist <= max_pixels

    def aim_and_attack(self, target_bbox: Optional[Tuple[int, int, int, int]]) -> None:
        if target_bbox is None:
            return

        cx, cy = self._screen_center()
        tx, ty = (target_bbox[0] + target_bbox[2]) // 2, (target_bbox[1] + target_bbox[3]) // 2
        dx = tx - cx
        dy = ty - cy

        self.mover.move_view(dx, dy)

        if self.is_attackable(target_bbox) and hasattr(self.attacker, "basic_attack"):
            self.attacker.basic_attack(times=2)

