import cv2 as cv

import os

import state_check.src as state 


class EventsChecker:
    """
    Класс, который обрабатывает события, происходящие на экране (Вход в подземелье, старт испытания и так далее)
    Выставляет флаги относительно событий (True, False)
    """
    @staticmethod
    def check_invite_in_dungeon(frame: cv.typing.MatLike, event_type: str='invite') -> bool:
        """
        Функция ищет шаблон по указанному типу события в кадре
        """
        return state.event_listeners.check_clicable_event_button(frame, event_type)
    
    @staticmethod
    def check_activate_dungeon(frame: cv.typing.MatLike, event_type: str='activate') -> bool:
        """
        Функция ищет шаблон по указанному типу события в кадре
        """
        return state.event_listeners.check_clicable_event_button(frame, event_type)
    
