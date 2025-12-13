from Model.keyboard_and_mouse_controllers import KeyboardController

class MoveToTreeStrategy:
    """
    Очень простой сценарий:
    - бежим вперёд заданное время;
    - нажимаем F.
    """

    def __init__(self, keyboard: KeyboardController, run_time: float = 10.0):
        self.keyboard = keyboard
        self.run_time = run_time

    def run(self) -> None:
        # небольшой забег вперёд
        self.keyboard.hold_key('w', duration=self.run_time)

        # нажать F для взаимодействия
        self.keyboard.press_key(['f'])