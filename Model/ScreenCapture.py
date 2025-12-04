import threading
from queue import Queue
import time
import numpy as np
import pyautogui as pgui
import cv2
from typing import Optional


class ScreenCapture:
    
    def __init__(self, region=None, fps_limit=30):
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
            if not self.frame_queue.full():
                self.frame_queue.put(frame, timeout=0.01)
            
            elapsed = time.time() - start_time
            time.sleep(max(0, interval - elapsed))
    
    def _screenshot(self) -> np.ndarray:
        screenshot = pgui.screenshot(region=self.region)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    def get_frame(self) -> Optional[np.ndarray]:
        try:
            return self.frame_queue.get_nowait()
        except:
            return None
    
    def set_region(self, region):
        self.region = region
