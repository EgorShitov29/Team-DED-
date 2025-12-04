from typing import Callable, List
from dataclasses import dataclass
import time
import numpy as np

class BotViewModel:
    def __init__(self, model):
        self.model = model
        self.state = BotState()
        self._listeners: List[Callable] = []
        
    def add_listener(self, listener):
        self._listeners.append(listener)
    
    def notify(self):
        for listener in self._listeners:
            listener(self.state)
    
    def start(self):
        self.model.start_pipeline()
        self.state.is_running = True
        self._run_loop()
    
    def stop(self):
        self.model.stop_pipeline()
        self.state.is_running = False
    
    def _run_loop(self):
        """VM: ТОЛЬКО оркестрация + FPS"""
        frame_times = []
        start_time = time.time()
        
        while self.state.is_running:
            loop_start = time.time()
            
            processed = self.model.process_frame()
            
            if processed:
                self.state.enemies_detected = self.model.stats['detected_enemies']
                self.state.current_action = self.model.stats['curr_action']
            
            frame_times.append(time.time() - loop_start)
            if len(frame_times) > 10:
                self.state.fps = 1.0 / np.mean(frame_times)
                frame_times = []
            
            self.notify()
            time.sleep(0.04) 