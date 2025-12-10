import threading
from queue import Queue
import time
import numpy as np
import pyautogui as pgui
import cv2
from typing import Optional


class ScreenCapture:
    
    def __init__(self, fps_limit=30):
        self.region = region or (0, 0, *pgui.size())
        self.fps_limit = fps_limit
        self.frame_queue = Queue(maxsize=3)
        self._running = False
        self._thread = None
        
    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
    
    def _capture_loop(self):
        interval = 1.0 / self.fps_limit
        while self._running:
            start_time = time.time()
            frame = self._screenshot()
            frame_data = {
                'frame': frame,
                }
            if not self.frame_queue.full():
                self.frame_queue.put(frame_data, timeout=0.01)
            
            elapsed = time.time() - start_time
            time.sleep(max(0, interval - elapsed))

    def _screenshot(self) -> np.ndarray:
        screenshot = pgui.screenshot(region=self.region)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    def get_frame_data(self):
        try:
            return self.frame_queue.get_nowait()
        except:
            return None


class BattleScreenCapture(ScreenCapture):
    def __init__(self, fps_limit=30):
        super().__init__(fps_limit)
        
    def _capture_loop(self):
        interval = 1.0 / self.fps_limit
        while self._running:
            start_time = time.time()
            frame = self._screenshot()
            height, width = frame.shape[:2]
            
            frame_data = {
                'frame': frame,
                'health_bar': self._crop_health_bar(frame, width, height),
                'e_attack': self._crop_e(frame, width, height)
            }
            if not self.frame_queue.full():
                self.frame_queue.put(frame_data, timeout=0.01)
            
            elapsed = time.time() - start_time
            time.sleep(max(0, interval - elapsed))
    
    def _crop_e(self, frame, width, height):
        right_x = round(width * 0.91)
        bottom_y = round(height * 0.97)
        window_width = round(width * 0.05)
        window_height = round(height * 0.1)
        x1 = right_x - window_width
        y1 = bottom_y - window_height
        x2 = right_x
        y2 = bottom_y
        return frame[y1:y2, x1:x2]
    
    def _crop_health_bar(self, frame, width, height):
        bottom_y = height
        window_width = round(width * 0.1)
        window_height = round(height * 0.1)
        center_x = width // 2
        x1 = center_x - window_widht 
        y1 = bottom_y - window_height
        x2 = center_x + window_widht 
        y2 = bottom_y + window_height
        return frame[y1:y2, x1:x2]