import cv2 as cv
import easyocr
import numpy as np 


class FrameTextCoordinator:
    """
    Класс выполняет обработку текста с кадра при помоще OCR
    Позволяет вычислисть координаты найденных текстов на кадре
    """
    def __init__(self, frame: cv.typing.MatLike=None, lang: str='ru') -> None:
        self._frame = frame
        self.reader = easyocr.Reader([lang], gpu=False)

    @property
    def frame(self):
        return self.frame
    
    @frame.setter
    def frame(self, new_frame: cv.typing.MatLike):
        self._frame = new_frame

    def __prepare_frame(self) -> cv.typing.MatLike:
        """
        Подготовка кадра для чтения
        """
        prepared_frame = cv.cvtColor(self._frame, cv.IMREAD_GRAYSCALE)
        return prepared_frame

    def __read_text_from_frame(self, prepared_frame) -> list:
        """
        Чтение текста с кадра и сохранение списка текста с координатами        
        """
        text_on_frame = self.reader.readtext(prepared_frame)
        return text_on_frame

    def __get_dict(self, text_on_frame) -> dict:
        """
        Создание словаря формата: 
        ключ - текст, значение - координаты
        """
        text_coords = dict()
        for (bbox, text, prob) in text_on_frame:
            if prob >= 0.7:
                text_coords[text] = bbox
        return text_coords

    def get_only_text(self):
        prepared_frame = self.__prepare_frame()
        t_frame_list = self.__read_text_from_frame(prepared_frame)
        return t_frame_list

    def get_text_and_coords(self) -> dict:
        """
        Объединение приватных методов
        Возвращение словаря
        """
        prepared_frame = self.__prepare_frame()
        text_on_frame = self.__read_text_from_frame(prepared_frame)
        return self.__get_dict(text_on_frame)


if __name__ == '__main__':
    frame_reader = FrameTextReader(frame=cv.imread('/home/kalilinux/dev/genshin_photo/photo/screen_under_art_4.png'))
    print(frame_reader.get_text_and_coords())