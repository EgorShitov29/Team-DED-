import time
from typing import List, Tuple, Optional

class BattleStrategy:
    """
    Высокоуровневая стратегия боя.

    Работает с внешними компонентами:
    - grab_frame: получение кадра;
    - enemy_detector: детекция врагов (YOLO/segm/что угодно);
    - skill_controller: логика прожатия скиллов/ультов;
    - enemy_aimer: выбор цели и поворот камеры;
    - keyboard: движение персонажа (WASD).
    """

    def __init__(
        self,
        grab_frame,
        enemy_detector,
        skill_controller,
        state_tracker=None,
        enemy_aimer=None,
        keyboard=None,
    ) -> None:
        self.grab_frame = grab_frame
        self.enemy_detector = enemy_detector
        self.skill_controller = skill_controller
        self.state_tracker = state_tracker
        self.enemy_aimer = enemy_aimer
        self.keyboard = keyboard

    # ---------- базовые операции ----------

    def get_frame(self):
        """
        Кадр текущей сцены.
        """
        return self.grab_frame()

    def detect_enemies(self, frame) -> List[Tuple[int, int, int, int]]:
        """
        Обёртка над детектором врагов.
        Сюда при желании можно добавить пост-обработку (фильтрация по классу/дистанции).
        """
        bboxes = self.enemy_detector(frame)
        return bboxes

    # ---------- логика движения ----------

    def _run_forward(self, duration: float = 0.5, key: str = "w") -> None:
        """
        Простой бег вперёд по указанной клавише (по умолчанию W).
        Shift не трогаем — он уже включён в игре.
        """
        if self.keyboard is None:
            return
        self.keyboard.down_key(key)
        time.sleep(duration)
        self.keyboard.up_key(key)

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
        Централизованная точка вызова ротации умений + движение к врагам.
        """
        num_enemies = len(enemy_bboxes)

        if self._should_use_burst(num_enemies):
            self.skill_controller.use_burst()

        if self._should_use_skill(num_enemies):
            self.skill_controller.use_skills()

        if num_enemies > 0 and hasattr(self.skill_controller, "basic_attack"):
            self.skill_controller.basic_attack(times=2)

        # --- поворот к ближайшему врагу и бег вперёд на него ---
        if num_enemies > 0 and self.enemy_aimer is not None:
            target_bbox = self.enemy_aimer.select_target(enemy_bboxes)
            if target_bbox is not None:
                # повернуть камеру к цели (EnemyAimer сам использует mover.move_view)
                self.enemy_aimer.aim_and_attack(target_bbox)

                # если цель ещё далеко от центра — немного пробежать вперёд
                if not self.enemy_aimer.is_attackable(target_bbox):
                    self._run_forward(duration=0.5, key="w")

    # ---------- тик стратегии ----------

    def tick(self) -> List[Tuple[int, int, int, int]]:
        """
        Один тик боевой логики:
        - берём кадр;
        - детектим врагов;
        - обновляем состояние;
        - прожимаем нужные скиллы и двигаемся к врагам.

        Возвращаем список врагов для отображения/логирования.
        """
        frame = self.get_frame()
        enemies = self.detect_enemies(frame)

        if self.state_tracker is not None:
            self.state_tracker.update(frame=frame, enemies=enemies)

        self.use_skills_if_needed(frame, enemies)

        return enemies
