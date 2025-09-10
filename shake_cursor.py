import time
import ctypes
import pyautogui
import os
import sys

# Get path to bundled cursor file
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

BIG_CURSOR_PATH = os.path.join(base_path, "cursor.cur")

SPI_SETCURSORS = 0x0057
SPIF_SENDCHANGE = 0x02

def set_custom_cursor(cur_path):
    print(f"[DEBUG] Trying to set custom cursor: {cur_path}")
    if os.path.exists(cur_path):
        hCursor = ctypes.windll.user32.LoadImageW(
            0, cur_path, 2, 0, 0, 0x00000010
        )
        if not hCursor:
            print("[ERROR] Failed to load cursor image.")
            return
        result = ctypes.windll.user32.SetSystemCursor(hCursor, 32512)
        if not result:
            print("[ERROR] Failed to set custom cursor.")
        else:
            print("[DEBUG] Custom cursor set successfully.")
    else:
        print(f"[ERROR] Cursor file not found: {cur_path}")

def reset_cursor():
    print("[DEBUG] Resetting cursor to default.")
    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, 0, SPIF_SENDCHANGE)
    if not result:
        print("[ERROR] Failed to reset system cursors.")

prev_pos = pyautogui.position()
last_shake_time = 0
shake_threshold = 1500  # Pixels per second

try:
    print("[DEBUG] Starting mouse shake detection loop...")
    while True:
        time.sleep(0.05)
        curr_pos = pyautogui.position()
        dx = curr_pos[0] - prev_pos[0]
        dy = curr_pos[1] - prev_pos[1]
        speed = (dx ** 2 + dy ** 2) ** 0.5 / 0.05

        print(f"[DEBUG] Mouse speed: {speed:.2f}")

        if speed > shake_threshold:
            print("[DEBUG] Shake detected.")
            last_shake_time = time.time()
            set_custom_cursor(BIG_CURSOR_PATH)

        if time.time() - last_shake_time > 1:
            reset_cursor()

        prev_pos = curr_pos

except KeyboardInterrupt:
    print("[DEBUG] Keyboard interrupt caught.")
    reset_cursor()
    print("[DEBUG] Exiting cleanly.")
