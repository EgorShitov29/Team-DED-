import numpy as np
from typing import Optional

class EnemyAimer:
    """
    Класс, который вычисляет ближайшего врага и направление до него.
    Возвращает команды либо в виде клавиш, которые нужно нажать для перемещения,
    либо готовность к атаке. Необходимо поиграться с мертвой зоной, порогами
    """
    def __init__(self, screen_center: tuple[int, int], deadzone: int = 50):
        self.screen_width, self.screen_height = screen_size
        self.hero_center = np.array([
            self.screen_width // 2,
            int(self.screen_height * 0.6)
        ], dtype=np.int32)
        
        self.deadzone = deadzone
        
    def extract_enemies_from_detection(self, detection_data: dict) -> np.ndarray:
        """Получим координаты углов ббокса и классы. Переведем координаты с numpy array"""
        coords = []
        # На будущее
        class_names = []
        
        for data in detection_data.values():
            coords.append(data['coords'])
            class_names.append(data['class_name'])
        
        if not coords:
            return np.empty((0, 4), dtype=np.int32)
            
        bboxes = np.array(coords, dtype=np.int32)
        bboxes[:, 2:] = np.maximum(bboxes[:, 2:], bboxes[:, :2] + 1)
        
        return bboxes
    
    def bboxes_to_centers(self, bboxes: np.ndarray) -> np.ndarray:
        """Получаем центры каждого ббокса"""  
        return (bboxes[:, :2] + bboxes[:, 2:]) // 2
      
    def get_nearest_enemy(self, bboxes: np.ndarray) -> tuple[Optional[np.ndarray], int]:
        """Находит ближайший ббокс по отношению к герою через евклидово расстояние"""
        if len(bboxes) == 0:
            return None, np.iinfo(np.int32).max
            
        centers = self.bbox_centers(bboxes)
        distances = np.linalg.norm(centers - self.hero_center, axis=1).astype(np.int32)
        
        nearest_idx = np.argmin(distances)
        return bboxes[nearest_idx], int(distances[nearest_idx])
    
    def get_direction(self, bbox: np.ndarray) -> tuple[int, int]:
        """Направление в пикселях от ббокса до героя"""
        center = self.bbox_centers(bbox.reshape(1, -1))[0]
        dx = center[0] - self.hero_center[0]
        dy = center[1] - self.hero_center[1]
        return int(dx), int(dy)
    
    def get_normalized_direction(self, dx: int, dy: int) -> tuple[float, float]:
        """Нормализованный вектор направляения для упрощения условий по получению команд"""
        distance = max(1, int(np.linalg.norm([dx, dy])))

        if distance < self.deadzone:
            return 0.0, 0.0
            
        return dx / distance, dy / distance
    
    def get_movement_command(self, dx: int, dy: int) -> Optional[str]:
        """Получает команды в зависимости от значенией направления"""
        dx_norm, dy_norm = self.get_normalized_direction(dx, dy)
        
        if abs(dx_norm) < 0.15 and abs(dy_norm) < 0.15:
            return None

        if abs(dx_norm) > 0.3 and abs(dy_norm) > 0.3:
            if dx_norm > 0 and dy_norm < 0: return 'wd'
            if dx_norm < 0 and dy_norm < 0: return 'wa'
            if dx_norm > 0 and dy_norm > 0: return 'sd'
            if dx_norm < 0 and dy_norm > 0: return 'sa'

        if abs(dx_norm) > abs(dy_norm):
            return 'd' if dx_norm > 0 else 'a'
        else:
            return 'w' if dy_norm < 0 else 's'
    
    def is_attackable(self, bbox: np.ndarray) -> bool:
        """Враг в зоне атаки: расстояние < 150px. Опционально - отследить увеличение ббокса"""
        nearest_bbox, distance = self.get_nearest_enemy(bbox.reshape(1, -1))
        return self.get_movement_command(dx, dy)