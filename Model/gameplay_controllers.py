import time

import keyboard_and_mouse_controllers as controllers


class CameraMover:
    
    def __init__(self, mouse_controller=controllers.MouseMover()) -> None:
        self.mouse_controller = mouse_controller

    def move_camera(self, coords) -> None:
        self.mouse_controller.move_cursor_to_coords(coords)

class PhisAttack:

    def __init__(self, clicker=controllers.MouseClicker()) -> None:
        self.clicker = clicker

    def attack_combination(self, kick_count: int) -> None:
        for cnt in range(kick_count):
            time.sleep(0.001)
            self.clicker.click()

class Runner:

    def __init__(self, keybord_controller=controllers.KeyboardController()) -> None:
        self.keybord_controller =keybord_controller

    def start_run(self, key='shift') -> None:
        self.keybord_controller.start_run(key)

    def stop_run(self, key='shift') -> None:
        self.keybord_controller.stop_run(key)
    
class ElementalAttack:

    def __init__(self, keybord_controller=controllers.KeyboardController()) -> None:
        self.keybord_controller = keybord_controller

    def elemental_attack(self, key='e') -> None:
        self.keybord_controller.press_key(keys=[key])
    
    def ultimate_attack(self, key='q') -> None:
        self.keybord_controller.press_key(keys=[key])

class MoveController:

    def __init__(self, keybord_controller=controllers.KeyboardController(), key_to_press: str='w') -> None:
        self.keyboard_controller = keybord_controller
        self.key = key_to_press

    def short_move(self) -> None:
        self.keybord_controller.press_key(keys=[self.key])

    def long_move(self, flag) -> None:
        if flag:
            self.keyboard_controller.down_key(self.key)
        else:
            self.keyboard_controller.up_key(self.key)

