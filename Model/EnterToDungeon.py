import cv2 as cv

import .gameplay_core as core
import .state_check.src.event_listeners.check_clicable_event_button as check_button 

def enter_to_dungeon(frame: cv.typing.MatLike, event_type='invite'):
    flag_invite =  check_button(frame, event_type)
    if flag_invite:
        core.click_event()
    return flag_invite