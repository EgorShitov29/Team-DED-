import numpy as np


class Aimer:
    """
    Наводка на дерево. 
    Механика, как и в бою. Отслеживаем площадь ббокса.
    Если площадь превышает порог, мы можем предположить, что находимся рядом с деревом
    """
    def __init__(self, screen_center: tuple[int, int], deadzone: int=50):
        self.screen_width, self.screen_height = screen_size
        self.hero_center = np.array([
            self.screen_width // 2,
            int(self.screen_height * 0.6)
        ], dtype=np.int32)

    def extract(self, detection_data: dict):
        coords = []

        for data in detection_data.values():
            coords.append(data['coords'])

        if not coords:
            return np.empty((0, 4), dtype=np.int32)

        bboxes = np.array(coords, dtype=np.int32)
        bboxes[:, 2:] = np.maximum(bboxes[:, 2:], bboxes[:, :2] + 1)
        
        return bboxes

    def bboxes_to_centers(self, bboxes: np.ndarray) -> np.ndarray:
        """Получаем центры каждого ббокса"""  
        return (bboxes[:, :2] + bboxes[:, 2:]) // 2

    def get_direction(self, bbox: np.ndarray) -> tuple[int, int]:
        """Направление в пикселях от ббокса до героя"""
        center = self.bbox_centers(bbox.reshape(1, -1))[0]
        dx = center[0] - self.hero_center[0]
        dy = center[1] - self.hero_center[1]
        return int(dx), int(dy)
    
    def get_normalized_direction(self, dx: int, dy: int) -> tuple[float, float]:
        """Нормализованный вектор направляения для упрощения условий по получению команд"""
        distance = max(1, int(np.linalg.norm([dx, dy])))
            
        return dx / distance, dy / distance
    
    def _get_bbox_area(self, bbox):
        x1, y1, x2, y2 = bbox
        x = x2 - x1
        y = y2 - y1
        area = x*y
        return area

    def get_bbox_percent(self, bbox_area):
        screen_area = self.screen_width * self.screen_height
        percent = (bbox_area / screen_area) * 100
        return int(percent)

    def get_movement_command(self, dx: int, dy: int) -> Optional[str]:
        """Получает команды в зависимости от значенией направления"""
        dx_norm, dy_norm = self.get_normalized_direction(dx, dy)
        
        bbox = self.

        if abs(dx_norm) > 0.3 and abs(dy_norm) > 0.3:
            if dx_norm > 0 and dy_norm < 0: return 'wd'
            if dx_norm < 0 and dy_norm < 0: return 'wa'
            if dx_norm > 0 and dy_norm > 0: return 'sd'
            if dx_norm < 0 and dy_norm > 0: return 'sa'

        if abs(dx_norm) > abs(dy_norm):
            return 'd' if dx_norm > 0 else 'a'
        else:
            return 'w' if dy_norm < 0 else 's'
    
    def get_aim_command(self, detection_data: dict) -> Optional[str]:
        bbox = self.extract(detection_data)
        
        bbox_area = self._get_bbox_area(bbox)
        percent = self.get_bbox_percent(bbox_area)
        if percent > 40:
            return 'activate'
        
        dx, dy = self.get_di rection(nearest_bbox)
        return self.get_movement_command(dx, dy)