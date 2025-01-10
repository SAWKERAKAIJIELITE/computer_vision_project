import time
from typing import Any
import keyboard
import win32con
import win32gui


VK_LEFT = 0x25
VK_RIGHT = 0x27


def press_key_on_window(hwnds: list[Any], key: str):

    if hwnds:
        hwnd = hwnds[0]  # Assume we have only one window

        # Ensure the window is on top, not minimized, and maximized
        # bring_window_to_front(hwnd)

        keyboard.press(key)
        time.sleep(0.05)
        keyboard.release(key)

    else:
        print("No matching window found.")


def bring_window_to_front(hwnd):
    """
    Bring the window to the front, un-minimized if necessary, and maximize it

    Args:
        hwnd (_type_): _description_
    """

    if win32gui.IsIconic(hwnd):  # Check if the window is minimized
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore it

    win32gui.SetForegroundWindow(hwnd)  # Bring the window to the front

    time.sleep(0.1)  # Small delay to ensure the window is focused


def find_all_windows(name: str):
    """
    Find all windows matching the name

    Args:
        name (str): _description_

    Returns:
        _type_: _description_
    """

    result: list[Any] = []

    def winEnumHandler(hwnd: list[Any], ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == name:
            result.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)

    return result


WINDOW_NAME = "Play games, WIN REAL REWARDS! | GAMEE - Personal - Microsoft​ Edge"
window_handler: list[Any] = find_all_windows(WINDOW_NAME)


def press_key_multiple(move_direction: str, num_of_press: int):
    for _ in range(num_of_press):
        press_key_on_window(window_handler, move_direction)
