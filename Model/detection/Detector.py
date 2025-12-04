import ultralytics
from ultralytics import YOLO
import cv2 as cv
import numpy as np


class Detector:
    """
    Класс, который инициализирует модель для детекции врагов.
    Фильтрует увернность в предсказании модели (в большинсте случаев помогло избавиться от проблемы детекции персонажа как врага)
    Возвращает словарь из ббоксов, их координат названий классов
    """
    def __init__(self, model_weights: str) -> None:
        self.model = YOLO(model_weights)
        self.names = self.model.names

    def __model_predict(self, source_image: str) -> np.ndarray:
        predictions = self.model.predict(source=source_image)
        return predictions

    def __filter_confidence(self, confidence: float, border_percent: float=0.6) -> bool:
        return confidence > border_percent

    def __get_prediction_data(self, predict_results:list) -> dict:
        prediction_data = dict()
        for result in predict_results:
            for idx, box in enumerate(result.boxes, 0):
                if self.__filter_confidence(float(box.conf[0])):
                    data = dict()
                    x1, y1, x2, y2 = list(map(int, box.xyxy[0]))
                    data['coords'] = [x1, y1, x2, y2]
                    data['class_name'] = self.names[int(box.cls[0])]
                    prediction_data[f'box_{idx}'] = data
        return prediction_data

    def detect(self, source_image: cv.typing.MatLike) -> dict:
        predict = self.__model_predict(self.model, source_image)
        prediction_data = self.__get_prediction_data(predict)
        return prediction_data



