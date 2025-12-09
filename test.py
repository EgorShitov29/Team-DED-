from ViewModel.VM import GameViewModel
from View.Interface import BotInterface
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

class GameViewModel:
    def __init__(self):
        self.state = "battle"
        self.is_running = False
        self.listeners = []
    
    def add_listener(self, callback):
        """View регистрирует callback"""
        self.listeners.append(callback)
    
    def notify_all(self, data):
        """ViewModel → View (обновление UI)"""
        for callback in self.listeners:
            callback(data)
    
    def start(self):
        self.is_running = True
        self.notify_all({'is_running': True, 'state': self.state})
    
    def stop(self):
        self.is_running = False
        self.notify_all({'is_running': False})
    
    def switch_state(self, state_name):
        """View → ViewModel (данные из Combobox)"""
        self.state = state_name
        self.notify_all({'state': state_name, 'is_running': self.is_running})
        logger.debug(f'состояние сейчас - {self.state}; запущен - {self.is_running}')

vm = GameViewModel()
root = BotInterface(vm)
root.mainloop()