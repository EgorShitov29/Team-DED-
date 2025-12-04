import tkinter as tk

from PIL import Image, ImageTk


class BotInterface(tk.Tk):
    def __init__(self, view_model):
        super().__init__()
        self.vm = view_model
        self.vm.add_listener(self._update_ui)
        self._setup_ui()
    
    def _setup_ui(self):
        self.title('autofight')
        self.geometry('350x250')
        
        tk.Button(self, text="START", command=self.vm.start, bg='green').pack(pady=10)
        tk.Button(self, text="STOP", command=self.vm.stop, bg='red').pack(pady=5)
        
        self.status_label = tk.Label(self, text="Готов", font=('Arial', 12))
        self.status_label.pack(pady=20)
    
    def _update_ui(self, state):
        if state.is_running:
            self.status_label.config(
                text=f"Врагов: {state.enemies_detected}",
                fg='green'
            )
        else:
            self.status_label.config(text="Остановка", fg='gray')
    
def use_attrs():
    root.attributes('-alpha', 0.3)
    root.attributes('-topmost', True)

if __name__ == '__main__':
    root = Interface()
    root.after(100, use_attrs)
    print(root.button_click)
    root.mainloop()