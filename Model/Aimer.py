from typing import Tuple


class Aimer:
    """
    Универсальный класс для выдачи команд движения/поворота к целевой точке.
    """

    def __init__(self, screen_size: Tuple[int, int], sensitivity: float, mover) -> None:
        self.screen_w, self.screen_h = screen_size
        self.sensitivity = sensitivity
        self.mover = mover  # объект, который умеет двигать мышь/камеру

    def _screen_center(self) -> Tuple[int, int]:
        return self.screen_w // 2, self.screen_h // 2

    def get_direction(self, target: Tuple[int, int]) -> Tuple[int, int]:
        """
        Возвращает (dx, dy) в пикселях от центра экрана до цели.
        """
        cx, cy = self._screen_center()
        tx, ty = target
        dx = tx - cx
        dy = ty - cy
        return dx, dy

    def get_movement_command(self, target: Tuple[int, int]) -> Tuple[int, int]:
        """
        Масштабирует (dx, dy) с учётом чувствительности, чтобы можно было
        передать дальше в контроллер ввода.
        """
        dx, dy = self.get_direction(target)
        move_x = int(dx * self.sensitivity)
        move_y = int(dy * self.sensitivity)
        return move_x, move_y

    def aim_to(self, target: Tuple[int, int]) -> None:
        """
        Высокоуровневая команда: повернуть камеру на цель.
        """
        move_x, move_y = self.get_movement_command(target)
        self.mover.move_view(move_x, move_y)
