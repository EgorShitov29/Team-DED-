from Model.keyboard_and_mouse_controllers import KeyboardController
import time

class SimpleEnterToDungeon:
    def __init__(self, keyboard: KeyboardController, run_time: float = 1.5):
        self.keyboard = keyboard
        self.run_time = run_time

    def enter(self) -> bool:
        print("[SimpleEnter] run forward (Shift)")
        self.keyboard.hold_key("shift", duration=self.run_time)
        time.sleep(0.3)
        print("[SimpleEnter] press F")
        self.keyboard.press_and_release("f")
        return True

