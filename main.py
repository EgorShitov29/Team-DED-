from Model.ActivateDungeon import ActivateDungeon
from Model.detection.Detector import Detector
from Model.Aimer import Aimer
from Model.BattleStrategy import BattleStrategy
from Model.CharacterStateChecker import CharacterStateChecker
from Model.CollectItemsStrategy import CollectItemsStrategy
from Model.CharacterStateServices import HealthService
from Model.collectors import CollectorController
from Model.SimpleCollect import MoveToTreeStrategy
from Model.ConfirmSquadBuild import ConfirmSquadBuild
from Model.DataCollector import DataCollector
from Model.DungeonModel import DungeonModel
from Model.EnemyAimer import EnemyAimer
from Model.Simple_EnterToDungeon import SimpleEnterToDungeon
from Model.EventsChecker import EventsChecker
from Model.FrameTextCoordinator import FrameTextCoordinator
from Model.gameplay_core import gameplay
from Model.keyboard_and_mouse_controllers import MouseMover,MouseClicker,KeyboardController
from Model.LevelSelector import LevelSelector
from Model.ScreenCapture import ScreenCapture
from Model.StateMachine import GameplayStateMachine
from Model.ToCharacterData import ToCharacterData
from Model import window_manager

from View.Interface import BotInterface

from ViewModel.DataStreamer import DataStreamer
from ViewModel.VM import GameViewModel

import threading
import time

def build_model():
    # --- окно Genshin и захват экрана ---
    left, top, right, bottom = window_manager.get_window_rect()
    w = right - left
    h = bottom - top

    screen = ScreenCapture(fps_limit=30, region=(left, top, w, h))
    screen.start()

    def grab_frame():
        data = screen.get_frame_data()
        if data is None:
            return None
        return data["frame"]

    # --- OCR / текст ---
    frame_text = FrameTextCoordinator()

    # --- состояние персонажа ---
    health_service = HealthService()
    state_checker = CharacterStateChecker()
    to_char_data = ToCharacterData()

    # --- ввод ---
    mouse_mover = MouseMover()
    mouse_clicker = MouseClicker()
    keyboard = KeyboardController()

    # --- события/кнопки и окна ---
    events_checker = EventsChecker()
    level_selector = LevelSelector()
    confirm_squad = ConfirmSquadBuild(
        grab_frame=grab_frame,
        frame_text=frame_text,
        clicker=mouse_clicker,
    )
    activate_dungeon = ActivateDungeon(
        grab_frame=grab_frame,
        frame_text=frame_text,
        clicker=mouse_clicker,
    )

    # простой сценарий входа: бежим вперёд и жмём F
    simple_enter = SimpleEnterToDungeon(keyboard=keyboard)

    # --- модель подземелья ---
    dungeon_model = DungeonModel()

    # --- YOLO-детектор врагов ---
    detector = Detector("Model/detection/weights/best.pt")

    def enemy_detector(frame):
        if frame is None:
            return []
        prediction_data = detector.detect(frame)
        bboxes = []
        for data in prediction_data.values():
            coords = data.get("coords")
            if coords and len(coords) == 4:
                x1, y1, x2, y2 = coords
                bboxes.append((int(x1), int(y1), int(x2), int(y2)))
        return bboxes

    # --- скилл-контроллер ---
    class SkillController:
        def __init__(self, kb: KeyboardController):
            self.kb = kb

        def use_burst(self):
            self.kb.press_key(['q'])

        def use_skills(self):
            self.kb.press_key(['e'])

    skill_controller = SkillController(keyboard)

    # --- боевая стратегия ---
    battle_strategy = BattleStrategy(
        grab_frame=grab_frame,
        enemy_detector=enemy_detector,
        skill_controller=skill_controller,
        state_tracker=None,
    )

    # --- FSM (пока просто создаём) ---
    fsm = GameplayStateMachine()

    return {
        "screen": screen,
        "dungeon_model": dungeon_model,
        "battle_strategy": battle_strategy,
        "fsm": fsm,
        "level_selector": level_selector,
        "confirm_squad": confirm_squad,
        "activate_dungeon": activate_dungeon,
        "simple_enter": simple_enter,
        "keyboard": keyboard,
    }

def run_bot_loop(vm: GameViewModel, deps: dict):
    screen: ScreenCapture = deps["screen"]
    battle_strategy: BattleStrategy = deps["battle_strategy"]
    simple_enter: SimpleEnterToDungeon = deps["simple_enter"]
    keyboard: KeyboardController = deps["keyboard"]

    while True:
        if not vm.is_running:
            time.sleep(0.1)
            continue

        state = vm.state

        if state == "battle":
            enemies = battle_strategy.tick()
            vm.notify_all(
                {
                    "state": state,
                    "is_running": True,
                    "enemies_detected": len(enemies),
                }
            )

        elif state == "enter_to_dungeon":
            # твой сценарий: стоим у двери, подбегаем вперёд и жмём F
            simple_enter.enter()
            vm.notify_all(
                {
                    "state": state,
                    "is_running": True,
                    "enemies_detected": 0,
                }
            )

        else:
            vm.notify_all(
                {
                    "state": state,
                    "is_running": True,
                    "enemies_detected": 0,
                }
            )

        time.sleep(0.05)

def main():
    # активируем окно игры
    window_manager.ensure_game_active()

    deps = build_model()
    vm = GameViewModel()

    ui = BotInterface(view_model=vm)

    bot_thread = threading.Thread(target=run_bot_loop, args=(vm, deps), daemon=True)
    bot_thread.start()

    ui.mainloop()


if __name__ == "__main__":
    main()

