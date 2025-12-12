class DungeonModel:
    """
    Хранит высокоуровневое состояние цикла подземелья.
    """

    def __init__(self) -> None:
        self._in_dungeon = False
        self._squad_confirmed = False
        self._battle_finished = False
        self._loot_collected = False
        self._health_ratio = None  # 0..1 или None

    def in_dungeon(self) -> bool:
        return self._in_dungeon

    def set_in_dungeon(self, value: bool) -> None:
        self._in_dungeon = value

    def squad_confirmed(self) -> bool:
        return self._squad_confirmed

    def set_squad_confirmed(self, value: bool) -> None:
        self._squad_confirmed = value

    def is_battle_finished(self) -> bool:
        return self._battle_finished

    def set_battle_finished(self, value: bool) -> None:
        self._battle_finished = value

    def is_loot_collected(self) -> bool:
        return self._loot_collected

    def set_loot_collected(self, value: bool) -> None:
        self._loot_collected = value

    def get_health_ratio(self):
        return self._health_ratio

    def set_health_ratio(self, value) -> None:
        self._health_ratio = value

    def reset_for_next_run(self) -> None:
        self._in_dungeon = False
        self._squad_confirmed = False
        self._battle_finished = False
        self._loot_collected = False
