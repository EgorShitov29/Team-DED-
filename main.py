import threading
import time

import pyautogui as pgui

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
from Model.SimpleEnterToDungeon import SimpleEnterToDungeon
from Model.EventsChecker import EventsChecker
from Model.FrameTextCoordinator import FrameTextCoordinator
from Model.gameplay_core import gameplay
from Model.keyboard_and_mouse_controllers import MouseMover, MouseClicker, KeyboardController
from Model.LevelSelector import LevelSelector
from Model.ScreenCapture import ScreenCapture
from Model.StateMachine import GameplayStateMachine
from Model.ToCharacterData import ToCharacterData
from Model import window_manager
from View.Interface import BotInterface
from ViewModel.DataStreamer import DataStreamer
from ViewModel.VM import GameViewModel


class CameraMover:
    def move_view(self, dx: int, dy: int) -> None:
        """
        Двигает мышь относительно текущей позиции для поворота камеры.
        """
        x, y = pgui.position()
        pgui.moveTo(x + dx, y + dy, duration=0.05)


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

    # --- сценарий входа в подземелье из модуля ---
    # ВАЖНО: подгони аргументы под реальный __init__ в Model/SimpleEnterToDungeon.py
    simple_enter = SimpleEnterToDungeon(
        keyboard=keyboard,
        events_checker=events_checker,
        activate_dungeon=activate_dungeon,
        frame_text=frame_text,
        grab_frame=grab_frame,
    )

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

        print("[YOLO] bboxes:", len(bboxes))
        return bboxes

    # --- скилл-контроллер ---
    class SkillController:
        def __init__(self, kb: KeyboardController, mouse: MouseClicker):
            self.kb = kb
            self.mouse = mouse

        def use_burst(self):
            print("[SkillController] use_burst (Q)")
            self.kb.press_key(["q"])

        def use_skills(self):
            print("[SkillController] use_skills (E)")
            self.kb.press_key(["e"])

        def basic_attack(self, times: int = 1):
            for _ in range(times):
                self.mouse.click()

    skill_controller = SkillController(keyboard, mouse_clicker)

    # --- camera mover + enemy aimer ---
    camera_mover = CameraMover()
    screen_w, screen_h = w, h

    enemy_aimer = EnemyAimer(
        screen_size=(screen_w, screen_h),
        mover=camera_mover,
        attacker=skill_controller,
    )

    # --- боевая стратегия ---
    battle_strategy = BattleStrategy(
        grab_frame=grab_frame,
        enemy_detector=enemy_detector,
        skill_controller=skill_controller,
        state_tracker=None,
        enemy_aimer=enemy_aimer,
        keyboard=keyboard,
    )

    # --- FSM ---
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
            if enemies:
                keyboard.hold_key("shift", duration=0.3)

            vm.notify_all(
                {
                    "state": state,
                    "is_running": True,
                    "enemies_detected": len(enemies),
                }
            )

        elif state == "enter_to_dungeon":
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

    bot_thread = threading.Thread(
        target=run_bot_loop,
        args=(vm, deps),
        daemon=True,
    )
    bot_thread.start()

    ui.mainloop()


if __name__ == "__main__":
    main()
