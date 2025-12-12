from typing import Optional, Tuple


class EnterToDungeon:
    """
    Логика нахождения портала подземелья и входа в него.
    """

    def __init__(self, grab_frame, portal_detector, mover, interactor) -> None:
        self.grab_frame = grab_frame
        self.portal_detector = portal_detector  # callable(frame) -> bbox | None
        self.mover = mover                      # двигает персонажа/камеру
        self.interactor = interactor            # жмёт кнопку "войти / F"

    def locate_dungeon_portal(self, frame) -> Optional[Tuple[int, int, int, int]]:
        return self.portal_detector(frame)

    def enter_dungeon(self, max_attempts: int = 10) -> bool:
        """
        Пытается подойти к порталу и войти в подземелье.
        Возвращает True при успехе.
        """
        for _ in range(max_attempts):
            frame = self.grab_frame()
            bbox = self.locate_dungeon_portal(frame)
            if bbox is None:
                # можно добавить поворот камеры/шаг вперёд для поиска
                self.mover.search_step()
                continue

            x1, y1, x2, y2 = bbox
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # идём к порталу и взаимодействуем
            self.mover.move_to(cx, cy)
            self.interactor.interact()
            return True

        return False
