from typing import Dict, Any, Tuple, Optional

import cv2 as cv
import numpy as np
import pytesseract


class FrameTextCoordinator:
    """
    Координатор текста на кадре на базе pytesseract.
    Даёт:
    - полный словарь {text: {"bbox": (x1,y1,x2,y2), "conf": float}};
    - поиск текста по подстроке с возвратом bbox.
    """

    def __init__(self, min_confidence: float = 50.0) -> None:
        """
        min_confidence: минимальная уверенность pytesseract (0..100)
        """
        self.min_confidence = min_confidence

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """
        Препроцессинг кадра для OCR.
        """
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # _, gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        return gray

    def _run_ocr(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Вызывает pytesseract и возвращает результат image_to_data в виде dict.
        """
        gray = self._preprocess(frame)
        data = pytesseract.image_to_data(
            gray,
            output_type=pytesseract.Output.DICT,
            lang="rus+eng",
        )
        return data

    def _build_index(self, frame: np.ndarray) -> Dict[str, Dict[str, Any]]:
        """
        Преобразует вывод pytesseract в словарь вида:
        { text: {"bbox": (x1,y1,x2,y2), "conf": float}, ... }
        Если один и тот же текст встречается несколько раз,
        берётся запись с максимальной уверенностью.
        """
        data = self._run_ocr(frame)
        texts = data.get("text", [])
        confs = data.get("conf", [])
        xs = data.get("left", [])
        ys = data.get("top", [])
        ws = data.get("width", [])
        hs = data.get("height", [])

        index: Dict[str, Dict[str, Any]] = {}

        for i, raw_text in enumerate(texts):
            text = (raw_text or "").strip()
            if not text:
                continue

            try:
                conf = float(confs[i])
            except (ValueError, TypeError):
                conf = -1.0

            if conf < self.min_confidence:
                continue

            x, y, w, h = xs[i], ys[i], ws[i], hs[i]
            bbox = (int(x), int(y), int(x + w), int(y + h))

            if text not in index or index[text]["conf"] < conf:
                index[text] = {"bbox": bbox, "conf": conf}

        return index

    # -------- публичное API --------

    def get_text_dict(self, frame: np.ndarray) -> Dict[str, Dict[str, Any]]:
        """
        Возвращает полный словарь всех надписей на кадре.
        """
        return self._build_index(frame)

    def get_text_and_coords(
        self,
        frame: np.ndarray,
        query: str,
        partial: bool = True,
    ) -> Optional[Tuple[str, Tuple[int, int, int, int]]]:
        """
        Ищет текст по подстроке/полным совпадением и возвращает (text, bbox).
        Если ничего не найдено — None.
        """
        index = self._build_index(frame)
        query_lower = query.lower()

        best_text = None
        best_bbox = None
        best_conf = -1.0

        for text, info in index.items():
            t_lower = text.lower()

            if partial:
                if query_lower not in t_lower:
                    continue
            else:
                if query_lower != t_lower:
                    continue

            conf = float(info.get("conf", 0.0))
            if conf > best_conf:
                best_conf = conf
                best_text = text
                best_bbox = info.get("bbox")

        if best_text is None or best_bbox is None:
            return None

        return best_text, best_bbox

    def has_text(self, frame: np.ndarray, query: str, partial: bool = True) -> bool:
        """
        Быстрая проверка наличия текста на экране.
        """
        return self.get_text_and_coords(frame, query, partial) is not None




