import pyautogui as pgui

import time

class MouseMover:
    
    def move_cursor_to_coords(self, coords: tuple[int, int], duration: float=0.1) -> None:
        pgui.moveTo(x=coords[0], y=coords[1], duration=duration)

class MouseClicker:
    
    def click(self) -> None:
        pgui.click()

class KeyboardController:
    
    def down_key(self, key: str) -> None:
        pgui.keyDown(key=key)

    def up_key(self, key: str) -> None:
        pgui.keyUp(key=key)
    
    def press_key(self, keys: list[str]) -> None:
        pgui.press(keys=keys)

    def hold_hotkey(self, keys_string: str, duration:float = 0.1) -> None:
        self.down_key(keys_string[0])
        self.down_key(keys_string[-1])
        time.sleep(duration)
        self.up_key(keys_string[0])
        self.up_key(keys_string[-1])
    
    def hold_key(self, keys_string: str, duration: float = 0.1) -> None:
        self.down_key(keys_string)
        time.sleep(duration)
        self.up_key(keys_string)