import pyautogui as pgui

import .state_check.src.search_text_frame as text_opp


class ConfirmSquadLevel:
    """
    Расширяемый класс. Но пока только два метода
    """
    def __init__(self, text_and_coords: dict):
        self.text_and_coords = text_and_coords

    def _find_squad_level(self, text: str) -> bool:
    """
    При помощи OCR ищем кнопку Начать
    """
    pattern = r'Начать'
    match = re.search(pattern, text)
    return match

    def start_with_confirmed_squad(self):
        for text in self.text_and_coords.keys():
            match = self._find_squad_level(text)
            if match:
                bbox = self.text_and_coords[text]
                centerx = (bbox[2] - bbox[0]) // 2
                centery = (bbox[3] - bbox[1]) // 2
                pgui.moveTo(x=centerx, y=centery)
                pgui.click()
                break
        return match