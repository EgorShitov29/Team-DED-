import pyautogui
import time
import subprocess
import sys


def get_platform():
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "macos"
    else:
        return "linux"


def activate_genshin_windows():
    try:
        import win32gui
        import win32con

        def find_genshin_hwnd():
            hwnd = win32gui.FindWindow("UnityWndClass", None)
            if not hwnd:
                # Пробуем найти по заголовку
                def callback(hwnd, extra):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if "Genshin Impact" in title:
                            extra.append(hwnd)
                    return True

                windows = []
                win32gui.EnumWindows(callback, windows)
                return windows[0] if windows else None
            return hwnd

        hwnd = find_genshin_hwnd()
        if hwnd:
            print("Нашел окно Genshin Impact, активирую...")

            # Развернуть если свернуто
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

            # Активировать окно
            win32gui.SetForegroundWindow(hwnd)

            # Двойной клик для гарантии
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            pyautogui.click(center_x, center_y)
            pyautogui.click(center_x, center_y)

            time.sleep(1)
            return True
        return False

    except ImportError:
        print("win32gui не установлен. Установите: pip install pywin32")
        return False


def activate_genshin_manual():
    print("Ручная активация игры...")

    # Сохраняем позицию курсора
    original_pos = pyautogui.position()

    # Кликаем несколько раз в центре
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    for i in range(3):
        pyautogui.click(center_x, center_y)
        time.sleep(0.2)

    # Возвращаем курсор
    pyautogui.moveTo(original_pos)
    time.sleep(1)
    return True


def ensure_game_active():
    platform = get_platform()

    if platform == "windows":
        if not activate_genshin_windows():
            print("Авто-активация не сработала, пробую ручной метод...")
            return activate_genshin_manual()
        return True
    else:
        return activate_genshin_manual()