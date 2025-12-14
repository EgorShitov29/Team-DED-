import pyautogui as pgui
import time

class MouseMover:
    def move_cursor_to_coords(self, coords: tuple[int, int], duration: float = 0.1) -> None:
        pgui.moveTo(x=coords[0], y=coords[1], duration=duration)

class MouseClicker:
    def click(self) -> None:
        pgui.click()

    def down_button(self, button: str = "left") -> None:
        pgui.mouseDown(button=button)

    def up_button(self, button: str = "left") -> None:
        pgui.mouseUp(button=button)

class KeyboardController:
    def down_key(self, key: str) -> None:
        pgui.keyDown(key=key)

    def up_key(self, key: str) -> None:
        pgui.keyUp(key=key)

    def press_key(self, keys: list[str]) -> None:
        """
        Нажать по очереди список клавиш.
        """
        for k in keys:
            pgui.press(k)

    def hold_hotkey(self, keys_string: str, duration: float = 0.1) -> None:
        """
        Удержать комбинацию из двух клавиш, например 'w+d'.
        Ожидается строка длиной 2 или формат 'wd'.
        """
        if len(keys_string) < 2:
            self.hold_key(keys_string, duration)
            return
        first = keys_string[0]
        last = keys_string[-1]

        self.down_key(first)
        self.down_key(last)
        time.sleep(duration)
        self.up_key(first)
        self.up_key(last)

    def hold_key(self, key: str, duration: float = 0.1) -> None:
        self.down_key(key)
        time.sleep(duration)
        self.up_key(key)
