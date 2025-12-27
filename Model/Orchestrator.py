import time
from enum import Enum

from .DungeonModel import DungeonModel
from .EnterToDungeon import EnterToDungeon
from .ActivateDungeon import ActivateDungeon
from .ConfirmSquadBuild import ConfirmSquadBuild
from .BattleStrategy import BattleStrategy
from .EnemyAimer import EnemyAimer
from .collectors import CollectorController


class BotState(Enum):
    IDLE = 0
    ENTER_DUNGEON = 1
    CONFIRM_SQUAD = 2
    IN_BATTLE = 3
    COLLECT_ITEMS = 4
    EXIT_OR_RESTART = 5
    STOPPED = 6


class Orchestrator:
    """
    Высокоуровневый оркестратор цикла:
    вход в подземелье -> подтверждение пачки -> бой -> сбор лута -> повтор/выход.
    """

    def __init__(
        self,
        dungeon_model: DungeonModel,
        enter_to_dungeon: EnterToDungeon,
        activator: ActivateDungeon,
        squad_confirmer: ConfirmSquadBuild,
        battle_strategy: BattleStrategy,
        enemy_aimer: EnemyAimer,
        collector: CollectorController,
        loop_delay: float = 0.2,
    ) -> None:
        self.dungeon_model = dungeon_model
        self.enter_to_dungeon = enter_to_dungeon
        self.activator = activator
        self.squad_confirmer = squad_confirmer
        self.battle_strategy = battle_strategy
        self.enemy_aimer = enemy_aimer
        self.collector = collector

        self.state = BotState.IDLE
        self.loop_delay = loop_delay
        self._running = False

    def start(self) -> None:
        self._running = True
        self.state = BotState.ENTER_DUNGEON

    def stop(self) -> None:
        self._running = False
        self.state = BotState.STOPPED

    def _step_enter_dungeon(self) -> None:
        if self.dungeon_model.in_dungeon():
            self.state = BotState.CONFIRM_SQUAD
            return

        entered = self.enter_to_dungeon.enter_dungeon()
        if entered:
            self.dungeon_model.set_in_dungeon(True)
            self.state = BotState.CONFIRM_SQUAD

    def _step_confirm_squad(self) -> None:
        if self.dungeon_model.squad_confirmed():
            self.state = BotState.IN_BATTLE
            return

        self.activator.open_start_menu()
        confirmed = self.squad_confirmer.wait_and_confirm()
        if confirmed:
            self.dungeon_model.set_squad_confirmed(True)
            self.state = BotState.IN_BATTLE

    def _step_battle(self) -> None:
        if self.dungeon_model.is_battle_finished():
            self.state = BotState.COLLECT_ITEMS
            return

        frame = self.battle_strategy.grab_frame()
        enemies = self.battle_strategy.detect_enemies(frame)
        target = self.enemy_aimer.select_target(enemies)
        self.enemy_aimer.aim_and_attack(target)

    def _step_collect_items(self) -> None:
        if self.dungeon_model.is_loot_collected():
            self.state = BotState.EXIT_OR_RESTART
            return

        self.collector.collect_after_battle()

    def _step_exit_or_restart(self) -> None:
        """
        Здесь можно реализовать:
        - выход в меню
        - повтор подземелья
        Пока просто сбрасываем флаги и возвращаемся к ENTER_DUNGEON.
        """
        self.dungeon_model.reset_for_next_run()
        self.state = BotState.ENTER_DUNGEON

    def run(self) -> None:
        """
        Главный цикл бота.
        """
        self.start()
        while self._running:
            if self.state == BotState.ENTER_DUNGEON:
                self._step_enter_dungeon()
            elif self.state == BotState.CONFIRM_SQUAD:
                self._step_confirm_squad()
            elif self.state == BotState.IN_BATTLE:
                self._step_battle()
            elif self.state == BotState.COLLECT_ITEMS:
                self._step_collect_items()
            elif self.state == BotState.EXIT_OR_RESTART:
                self._step_exit_or_restart()
            elif self.state == BotState.STOPPED:
                break

            time.sleep(self.loop_delay)
