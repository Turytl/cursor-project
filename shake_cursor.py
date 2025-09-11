import time
import ctypes
import os
import sys

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

SPI_SETCURSORS = 0x0057
SPIF_SENDCHANGE = 0x02

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

BIG_CURSOR_PATH = os.path.join(base_path, "cursor.cur")

def get_cursor_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def set_custom_cursor(cur_path):
    if os.path.exists(cur_path):
        hCursor = ctypes.windll.user32.LoadImageW(0, cur_path, 2, 0, 0, 0x00000010)
        if hCursor:
            ctypes.windll.user32.SetSystemCursor(hCursor, 32512)

def reset_cursor():
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, 0, SPIF_SENDCHANGE)

prev_pos = get_cursor_pos()
last_shake_time = 0
shake_threshold = 3000  # Pixels per second
custom_active = False

try:
    while True:
        time.sleep(0.15)  # Increased interval
        curr_pos = get_cursor_pos()
        dx = curr_pos[0] - prev_pos[0]
        dy = curr_pos[1] - prev_pos[1]
        speed = (dx ** 2 + dy ** 2) ** 0.5 / 0.15

        if speed > shake_threshold:
            last_shake_time = time.time()
            if not custom_active:
                set_custom_cursor(BIG_CURSOR_PATH)
                custom_active = True

        elif time.time() - last_shake_time > 1:
            if custom_active:
                reset_cursor()
                custom_active = False

        prev_pos = curr_pos

except KeyboardInterrupt:
    reset_cursor()
