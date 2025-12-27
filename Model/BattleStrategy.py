from typing import List, Tuple, Optional


class BattleStrategy:
    """
    Высокоуровневая стратегия боя.
    Работает с внешними компонентами:
    - grab_frame: получение кадра;
    - enemy_detector: детекция врагов (YOLO/segm/что угодно);
    - skill_controller: логика прожатия скиллов/ультов.
    """

    def __init__(
        self,
        grab_frame,
        enemy_detector,
        skill_controller,
        state_tracker=None,
    ) -> None:
        self.grab_frame = grab_frame
        self.enemy_detector = enemy_detector
        self.skill_controller = skill_controller
        self.state_tracker = state_tracker

    # ---------- базовые операции ----------

    def get_frame(self):
        """
        Кадр текущей сцены.
        """
        return self.grab_frame()

    def detect_enemies(self, frame) -> List[Tuple[int, int, int, int]]:
        """
        Обёртка над детектором врагов.
        Сюда при желании можно добавить пост‑обработку (фильтрация по классу/дистанции).
        """
        bboxes = self.enemy_detector(frame)
        return bboxes

    # ---------- логика скиллов ----------

    def _should_use_burst(self, num_enemies: int) -> bool:
        """
        Пример простой эвристики.
        Если у тебя есть своя логика (по ХП, фазам, кулдаунам) — перенеси её сюда.
        """
        return num_enemies >= 3

    def _should_use_skill(self, num_enemies: int) -> bool:
        return num_enemies >= 1

    def use_skills_if_needed(self, frame, enemy_bboxes: List[Tuple[int, int, int, int]]) -> None:
        """
        Централизованная точка вызова ротации умений.
        """
        num_enemies = len(enemy_bboxes)

        if self._should_use_burst(num_enemies):
            self.skill_controller.use_burst()

        if self._should_use_skill(num_enemies):
            self.skill_controller.use_skills()

    # ---------- тик стратегии ----------

    def tick(self) -> List[Tuple[int, int, int, int]]:
        """
        Один тик боевой логики:
        - берём кадр;
        - детектим врагов;
        - обновляем состояние;
        - прожимаем нужные скиллы.
        Возвращаем список врагов для EnemyAimer/Orchestrator.
        """
        frame = self.get_frame()
        enemies = self.detect_enemies(frame)

        if self.state_tracker is not None:
            self.state_tracker.update(frame=frame, enemies=enemies)

        self.use_skills_if_needed(frame, enemies)
        return enemies
