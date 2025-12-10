import cv2 as cv
import pyautogui as pgui

import gameplay_core as core
from keyboard_and_mouse_controllers import KeyboardController
import state_check.src.event_listeners.check_clicable_event_button as check_button 

def get_frame():
    frame = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return frame

def activate_dungeon(event_type='activate'):
    flag_activate = False
    
    while not(flag_activate):
        KeyboardController.hold_key('w')
        frame = get_frame()
        flag_activate = check_button(frame, event_type)
    
    return flag_activate

