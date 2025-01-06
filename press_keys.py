import time
import win32api
import win32con
import win32gui

# Key codes for Left and Right Arrow keys
VK_LEFT = 0x25  # Virtual key code for Left arrow
VK_RIGHT = 0x27  # Virtual key code for Right arrow

def press_key_on_window(hwnds, key):
    # Window name
    # hwnds = find_all_windows(window_name)

    if hwnds:
        hwnd = hwnds[0]  # Assume we have only one window
        # Ensure the window is on top, not minimized, and maximized
        bring_window_to_front(hwnd)
        # Perform key presses (only left and right arrow keys)
        if key == 'left':
            press_key(hwnd, VK_LEFT, 0.05, 0.05)   # Left arrow press
            # press_key(hwnd, VK_LEFT, 0.01, 0.01)   # Left arrow press
            # press_key(hwnd, VK_LEFT, 0.01, 0.01)   # Left arrow press
        if key ==  'right':
            press_key(hwnd, VK_RIGHT, 0.05, 0.05)  # Right arrow press
    else:
        print("No matching window found.")

# Bring the window to the front, un-minimized if necessary, and maximize it
def bring_window_to_front(hwnd):
    # Check if the window is minimized and restore it if necessary
    if win32gui.IsIconic(hwnd):  # Check if the window is minimized
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore it if minimized
    # win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # Maximize the window
    win32gui.SetForegroundWindow(hwnd)  # Bring the window to the front
    time.sleep(0.1)  # Small delay to ensure the window is focused

# Send a key press to the window
def press_key(hwnd, key, start_sec, hold_sec):
    # Wait before pressing the key
    time.sleep(start_sec)

    # Key down event
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
    time.sleep(hold_sec)

    # Key up event
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, key, 0)

# Find all windows matching the name
def find_all_windows(name):
    result = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == name:
            result.append(hwnd)
    win32gui.EnumWindows(winEnumHandler, None)
    return result

window_name = "Play games, WIN REAL REWARDS! | GAMEE - Personal - Microsoft​ Edge"
window_handler = find_all_windows(window_name)
# press_key_on_window(window_handler,'left')
# press_key_on_window(window_handler,'left')
# press_key_on_window(window_handler,'left')

def press_key_multiple(move_direction,num_of_press):
    for i in range(num_of_press) :
        press_key_on_window(window_handler,move_direction)