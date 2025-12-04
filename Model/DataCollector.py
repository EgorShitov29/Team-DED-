import threading
import time
from queue import Queue, Empty


class DataCollector:

    def __init__(self, data_queue: Queue):
        self.data_queue = data_queue
        self.flag_running = False
        self.thread = None

    def start_thread(self):
        self.flag_running = True
        self.thread = threading.Thread(target=self.collect, daemon=True)
        self.thread.start()
    
    def stop_thread(self):
        self.flag_running = False
        if self.thread:
            self.thread.join(timeout=1)

    def collect(self):
        pass