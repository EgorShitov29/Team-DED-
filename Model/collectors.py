from typing import Optional

from Model.CollectItemsStrategy import CollectItemsStrategy
from Model.DungeonModel import DungeonModel
from Model.FrameTextCoordinator import FrameTextCoordinator


class CollectorController:
    """
    Обёртка над CollectItemsStrategy + проверка необходимости хила.
    """

    def __init__(
        self,
        dungeon_model: DungeonModel,
        frame_text: FrameTextCoordinator,
        collect_strategy: CollectItemsStrategy,
        health_threshold: float = 0.4,
    ) -> None:
        self.dungeon_model = dungeon_model
        self.frame_text = frame_text
        self.collect_strategy = collect_strategy
        self.health_threshold = health_threshold

    def check_need_heal(self) -> bool:
        """
        Простейшая логика: берём значение из DungeonModel.
        При желании можно привязать к OCR полоски HP.
        """
        health_ratio = self.dungeon_model.get_health_ratio()
        return health_ratio is not None and health_ratio < self.health_threshold

    def collect_after_battle(self) -> None:
        """
        Запустить цикл сбора лута после завершения битвы.
        """
        if not self.dungeon_model.is_battle_finished():
            return
        self.collect_strategy.run_loop()
        self.dungeon_model.set_loot_collected(True)
