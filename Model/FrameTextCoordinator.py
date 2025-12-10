import cv2 as cv
import easyocr
import numpy as np 


class FrameTextCoordinator:
    """
    Класс выполняет обработку текста с кадра при помоще OCR
    Позволяет вычислисть координаты найденных текстов на кадре
    """
    def __init__(self, lang: str='ru') -> None:
        self.reader = easyocr.Reader([lang], gpu=False)

    def _prepare_frame(self, frame) -> cv.typing.MatLike:
        """
        Подготовка кадра для чтения
        """
        prepared_frame = cv.cvtColor(frame, cv.IMREAD_GRAYSCALE)
        return prepared_frame

    def _read_text_from_frame(self, prepared_frame) -> list:
        """
        Чтение текста с кадра и сохранение списка текста с координатами        
        """
        text_on_frame = self.reader.readtext(prepared_frame)
        return text_on_frame

    def _get_dict(self, text_on_frame) -> dict:
        """
        Создание словаря формата: 
        ключ - текст, значение - координаты
        """
        text_coords = dict()
        for (bbox, text, prob) in text_on_frame:
            if prob >= 0.7:
                text_coords[text] = bbox
        return text_coords

    def get_only_text(self, frame: cv.typing.MatLike):
        prepared_frame = self._prepare_frame(frame)
        t_frame_list = self._read_text_from_frame(prepared_frame)
        return t_frame_list

    def get_text_and_coords(self, frame: cv.typing.MatLike) -> dict:
        """
        Объединение приватных методов
        Возвращение словаря
        """
        prepared_frame = self._prepare_frame(frame)
        text_on_frame = self._read_text_from_frame(prepared_frame)
        return self.__get_dict(text_on_frame)