from Model.keyboard_and_mouse_controllers import KeyboardController

class SimpleEnterToDungeon:
    """
    Очень простой сценарий:
    - сделать шаг вперёд;
    - нажать F один раз.
    Предполагается, что ты уже стоишь прямо перед дверью.
    """

    def __init__(self, keyboard: KeyboardController) -> None:
        self.keyboard = keyboard

    def enter(self) -> bool:
        # небольшой шаг вперёд
        self.keyboard.hold_key('w', duration=1.5)

        # нажать F для входа
        self.keyboard.press_key(['f'])
        return True
