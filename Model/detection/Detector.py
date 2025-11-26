import ultralytics
from ultralytics import YOLO
import cv2 as cv
import numpy as np


class Detector:

    def __init__(self, model_weights: str) -> None:
        self.model_weights = model_weights

    def __init_model(self) -> ultralytics.models.yolo.model.YOLO:
        model = YOLO(self.model_weights)
        return model

    def __get_model_names(self, model: ultralytics.models.yolo.model.YOLO) -> dict:
        return model.names

    def __model_predict(self, model: YOLO, source_image: str) -> np.ndarray:
        predictions = model.predict(source=source_image)
        return predictions

    def __filter_confidence(self, confidence: float, border_percent: float=0.6) -> bool:
        return confidence > border_percent

    def __get_prediction_data(self, predict_results:list, model_names: dict) -> dict:
        prediction_data = dict()
        for result in predict_results:
            for idx, box in enumerate(result.boxes, 0):
                if self.__filter_confidence(float(box.conf[0])):
                    data = dict()
                    data['coords'] = list(map(int, box.xyxy[0]))
                    data['class_name'] = model_names[int(box.cls[0])]
                    data['confidence'] = float(box.conf[0])
                    prediction_data[f'box_{idx}'] = data
        return prediction_data

    def detect(self, source_image: str) -> None:
        model = self.__init_model()
        names = self.__get_model_names(model)
        predict = self.__model_predict(model, source_image)
        prediction_data = self.__get_prediction_data(predict, names)
        return prediction_data



