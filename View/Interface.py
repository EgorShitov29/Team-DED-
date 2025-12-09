import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

class BotInterface(tk.Tk):
    def __init__(self, view_model=None):
        super().__init__()
        self.vm = view_model
        if self.vm:
            self.vm.add_listener(self._update_ui)
        self._setup_ui()
        self._apply_attrs()

    def _setup_ui(self):
        self.title('Автобой')
        self.geometry('300x280')
        
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="Состояние:", font=('Arial', 10, 'bold')).pack(pady=(0,5))
        self.state_var = tk.StringVar(value="battle")
        states = [
            "enter_to_dungeon",
            "select_level", 
            "squad_build",
            "activate_dungeon",
            "battle"
        ]
        self.state_combo = ttk.Combobox(main_frame, textvariable=self.state_var, 
                                    values=states, state="readonly", width=20)
        self.state_combo.pack(pady=(0,15))
 
        self.state_combo.bind('<<ComboboxSelected>>', self._on_state_selected)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="Запуск", bg='#4CAF50', fg='white',
                                  font=('Arial', 10, 'bold'), width=10,
                                  command=self._on_start)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="Остановка", bg='#F44336', fg='white', 
                                 font=('Arial', 10, 'bold'), width=10,
                                 command=self._on_stop, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        ttk.Button(main_frame, text="Перейти", command=self._switch_state).pack(pady=10)
        
        self.status_label = tk.Label(main_frame, text="Готов", 
                                   font=('Arial', 12, 'bold'), fg='orange')
        self.status_label.pack(pady=(10,5))
        
        self.stats_label = tk.Label(main_frame, text="Врагов: 0", 
                                  font=('Arial', 9), fg='gray')
        self.stats_label.pack()
    
    def _on_state_selected(self, event):
        state_name = self.state_var.get()
        if self.vm:
            self.vm.switch_state(state_name)
    
    def _on_start(self):
        if self.vm:
            self.vm.start()
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
    
    def _on_stop(self):
        if self.vm:
            self.vm.stop()
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
    
    def _update_ui(self, data):
        enemies = data.get('enemies_detected', 0)
        running = data.get('is_running', False)
        state = data.get('state', 'battle')
        
        self.stats_label.config(text=f"Врагов: {enemies}")
        self.status_label.config(
            text=f"🟢 {state}" if running else "Остановлен",
            fg='green' if running else 'gray'
        )
    
    def _switch_state(self):
        state_name = self.state_var.get()
        state_map = {
            "Войти в подземелье": "enter_to_dungeon",
            "Выбрать уровень": "select_level",
            "Билд отряда": "squad_build",
            "Активация подземелья": "activate_dungeon",
            "Бой": "battle"
        }
        target_state = state_map.get(state_name)
        if target_state and self.vm:
            self.vm.switch_state(target_state)
    
    def _apply_attrs(self):
        self.attributes('-alpha', 0.9)
        self.attributes('-topmost', True)
    
    
    def _apply_attrs(self):
        """Прозрачность + поверх всех окон"""
        self.attributes('-alpha', 0.7)
        self.attributes('-topmost', True)
    

def use_attrs():
    root.attributes('-alpha', 0.3)

if __name__ == "__main__":
    class MockVM:
        def start(self): print("START")
        def stop(self): print("STOP") 
        def switch_state(self, state): print(f"STATE: {state}")
    
    root = BotInterface(MockVM())
    root.mainloop()
