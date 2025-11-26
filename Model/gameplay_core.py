import time

import keyboard_and_mouse_controllers as controllers


def move_camera(coords, mouse_controller=controllers.MouseMover()) -> None:
    mouse_controller.move_cursor_to_coords(coords)

def attack_combination(kick_count: int, clicker=controllers.MouseClicker()) -> None:
    for cnt in range(kick_count):
        time.sleep(0.001)
        clicker.click()

def start_run(key='shift', keybord_controller=controllers.KeyboardController()) -> None:
    keybord_controller.up_key(key)

def stop_run(key='shift', keybord_controller=controllers.KeyboardController()) -> None:
    keybord_controller.down_key(key)

def change_charecter(key=any(['1', '2', '3', '4']), keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.press_key([key])

def click_event(key='f', keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.press_key([key])

def elemental_attack(key='e', keybord_controller=controllers.KeyboardController()) -> None:
    keybord_controller.press_key(keys=[key])

def ultimate_attack(key='q', keybord_controller=controllers.KeyboardController()) -> None:
    keybord_controller.press_key(keys=[key])

def short_move(key_to_press: str='w', keybord_controller=controllers.KeyboardController()) -> None:
    keybord_controller.press_key(keys=[key_to_press])

def long_move(flag, key_to_press: str='w', keybord_controller=controllers.KeyboardController()) -> None:
    if flag:
        keybord_controller.down_key(key_to_press)
    else:
        keybord_controller.up_key(key_to_press)
