import cv2 as cv
import numpy as numpy
import pyautogui as pgui

import os
import json


def check_clicable_event_button(frame: cv.typing.MatLike, event_type: str) -> bool:
    """
    функция по типу отслеживаемого ивента (action)
    подбирает подходящий шаблон и ищет его на кадре (frame)
    Если шаблон найден, и он находится по Y около половины высоты кадра,
    тогда выводим, что можно жать на кнопку
    """
    # И кадр, и шаблон - в градацию серого
    template = cv.imread(f'../static/{event_type}_template.png', cv.IMREAD_GRAYSCALE)
    if template is None:
        return False
    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    im_h = img_gray.shape[0]
    center = im_h // 2
    percent = round(im_h * 0.2)
    w, h = template.shape[::-1]

    # Методы поиска
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED',
               'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']

    # Используя все методы поиска, ищем шаблон на кадре
    for meth in methods:
        img = img_gray.copy()
        method = getattr(cv, meth)

        res = cv.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

    # Смотрим на положение шаблона в кадре. Если удовлетворяет условию, то вернет True
    if all((center + percent) > y > (center - percent) for y in (top_left[1], bottom_right[1])):
        return True

    return False
