import time
import pyautogui as pgui
from . import keyboard_and_mouse_controllers as controllers


def move_camera(coords, mouse_controller=controllers.MouseMover()) -> None:
    mouse_controller.move_cursor_to_coords(coords)

def attack_combination(kick_count: int, clicker=controllers.MouseClicker()) -> None:
    for cnt in range(kick_count):
        time.sleep(0.01)
        clicker.click()

def start_run(key='shift', keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.down_key(key)

def stop_run(key='shift', keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.up_key(key)

def dash_forward(key='shift', keyboard_controller=controllers.KeyboardController()):
    keyboard_controller.press_key([key])

def change_character(slot: int = 1, keyboard_controller=controllers.KeyboardController()) -> None:
    key = str(slot)
    keyboard_controller.press_key([key])

def click_event(key='f', keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.press_key([key])

def elemental_attack(key='e', keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.press_key([key])

def ultimate_attack(key='q', keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.press_key([key])

def short_move(key_to_press: str='w', keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.press_key([key_to_press])

def diagonal_move(keys_string: str, keyboard_controller=controllers.KeyboardController()) -> None:
    keyboard_controller.hold_hotkey(keys_string, duration=0.2)

def long_move(flag, key_to_press: str='w', keyboard_controller=controllers.KeyboardController()) -> None:
    if flag:
        keyboard_controller.down_key(key_to_press)
    else:
        keyboard_controller.up_key(key_to_press)

