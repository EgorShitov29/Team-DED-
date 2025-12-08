import cv2 as cv

import re


def find_squad_level(text: str) -> None | int:
    """
    Функция ищет уровень отряда по паттерну
    Возвращает результат поиска: пустое значение либо число
    """
    pattern = r'ур\. отряда:\s*(\d+)'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return match

def confirm_squad_level(text: str) -> bool:
    """
    При помощи OCR ищем кнопку Начать
    """
    pattern = r'Начать'
    match = re.search(pattern, text)
    if match:
        return True
    return False

def find_closest(numbers, target):
    return min(numbers, key=lambda x: abs(x - target))

if __name__ == '__main__':
    test_lst = ['Рекомендуемый ур. отряда: 33', 'Начать', 'Рекомендуемый ур. отряда: 54', 
           'Рекомендуемый ур. отряда: 81', 'Ваше подземелье есть', 'Рекомендуемый ур. отряда: 89']
    for t in test_lst:
        match = confirm_squad_level(t)
        print(match)
