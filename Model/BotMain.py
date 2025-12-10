from DungeonModel import DungeonModel
from ViewModel.VM import GameViewModel

class BotMain:
    """
    Доделать этот классс. Это основной цикл бота
    """
    def __init__(self, model: DungeonModel, view_model: GameViewModel):
        self.model = model
        self.vm = view_model
        self.running = False
        self.thread = None
    
    def start_main_loop(self):
        self.running = True
        self.thread = threading.Thread(target=self._main_loop, daemon=True)
        self.thread.start()
    
    def _main_loop(self):
        while self.running:
            current_state = self.vm.state

            #Добавить и обработать методы из DungeonModel
            action_map = {

            }
            
            if current_state in action_map:
                try:
                    action_map[current_state]()
                except Exception as e:

            stats = self.model.battle_strategy.stat if hasattr(self.model.battle_strategy, 'stat') else {}
            self.vm.notify_all({
                'state': current_state,
                'is_running': self.running,
                **stats
            })
            
            time.sleep(1.0)
    
    def stop(self):
        self.running = False
        if self.model.battle_strategy:
            self.model.battle_strategy.stop()