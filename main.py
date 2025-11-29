from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import pyautogui
from get_game_state import detect_game_state
import pygetwindow as gw
from window_manager import ensure_game_active
import pyautogui
import time
from detection_enemy import detect_enemies, get_battle_strategy


class CombatBot:
    def __init__(self):
        self.current_state = "unknown"
        self.last_strategy = "none"
        self.activation_count = 0
        self.last_character_switch = 0
        self.min_switch_delay = 3  # сек между сменами персонажа

        # Шаблоны иконок элементов (загружаем заранее)
        self.templates = {
            'cryo': cv2.imread('templates/cryo_icon.png', cv2.IMREAD_COLOR),
            'hydro': cv2.imread('templates/hydro_icon.png', cv2.IMREAD_COLOR),
            'pyro': cv2.imread('templates/pyro_icon.png', cv2.IMREAD_COLOR),
            'electro': cv2.imread('templates/electro_icon.png', cv2.IMREAD_COLOR),
            # добавь остальные по необходимости
        }

        # Маппинг: элемент врага -> слот персонажа (1-4)
        self.counter_map = {
            'cryo': '2',  # Пиро против Крио
            'hydro': '3',  # Электро против Гидро
            'pyro': '4',  # Гидро против Пиро
            'electro': '1',  # Дендро против Электро
        }

    def detect_enemy_element(self, screenshot):
        """Детектирует элемент врага по иконке над HP"""
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Область поиска: верх экрана где иконки элементов (адаптируй под разрешение)
        search_region = frame[50:200, 100:frame.shape[1] - 100]  # y1:y2, x1:x2

        for element, template in self.templates.items():
            if template is None:
                continue

            result = cv2.matchTemplate(search_region, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            if max_val > 0.8:  # порог уверенности
                print(f"Обнаружен враг с элементом: {element}")
                return element

        return None

    def switch_character(self, slot):
        """Переключает на персонажа в слоте"""
        current_time = time.time()
        if current_time - self.last_character_switch < self.min_switch_delay:
            return False

        print(f"Переключаюсь на персонажа в слоте {slot}")
        self.safe_input("press", slot)
        time.sleep(0.5)  # ждем загрузки персонажа
        self.last_character_switch = current_time
        return True

    def safe_input(self, action, *args, **kwargs):
        # Переактивируем игру каждые 10 команд
        if self.activation_count % 10 == 0:
            ensure_game_active()

        self.activation_count += 1

        try:
            if action == "click":
                pyautogui.click(*args, **kwargs)
            elif action == "press":
                pyautogui.press(*args, **kwargs)
            elif action == "keyDown":
                pyautogui.keyDown(*args, **kwargs)
            elif action == "keyUp":
                pyautogui.keyUp(*args, **kwargs)
            return True
        except Exception as e:
            print(f"Ошибка ввода: {e}")
            return False

    def handle_battle(self, enemies):
        # *** НОВАЯ ЛОГИКА: проверяем элементы врагов ПЕРЕД стратегией ***
        screenshot = pyautogui.screenshot()
        enemy_element = self.detect_enemy_element(screenshot)

        if enemy_element and enemy_element in self.counter_map:
            slot = self.counter_map[enemy_element]
            self.switch_character(slot)
            # Даем время персонажу активироваться
            time.sleep(1)
            return  # пропускаем основную стратегию после смены

        # Обычная логика стратегии
        strategy = get_battle_strategy(enemies)
        if strategy != self.last_strategy:
            print(f"Смена стратегии: {strategy}")
            self.last_strategy = strategy

        if strategy == "focus_boss":
            print("Фокусируюсь на боссе!")
            self.safe_input("click", button='right')

        elif strategy == "focus_status_enemies":
            print("Фокусируюсь на врагах со статусами!")
            self.safe_input("press", 'e')

        elif strategy == "focus_normal_enemies":
            print("Атакую обычных врагов!")
            self.safe_input("click")

        else:
            print("Врагов не видно, продолжаю осмотр")
            self.safe_input("press", 'w')

    def handle_map(self):
        print("На карте, ищу точку входа в данж")
        self.safe_input("press", 'm')

    def handle_exploring(self):
        print("Исследую локацию...")
        self.safe_input("keyDown", 'w')
        time.sleep(1)
        self.safe_input("keyUp", 'w')

    def update(self, screenshot):
        state, data = detect_game_state(screenshot)

        if state != self.current_state:
            print(f"Смена состояния: {self.current_state} -> {state}")
            self.current_state = state

        # Обработка состояний
        if state == "battle":
            self.handle_battle(data)
        elif state == "map":
            self.handle_map()
        elif state == "exploring":
            self.handle_exploring()


def main():
    bot = CombatBot()
    time.sleep(5)

    # Первоначальная активация
    ensure_game_active()

    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n=== Итерация {iteration} ===")

            # Делаем скриншот
            screenshot = pyautogui.screenshot()

            # Обновляем состояние бота
            bot.update(screenshot)

            # Пауза между итерациями
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")


if __name__ == "__main__":
    main()
