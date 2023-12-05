import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))
import win32api
import win32con
import pyautogui
import time

from package.mouse_operation.mouse_move import MouseMove


class MouseDrag(object):
    def __init__(self):
        pass

    @staticmethod
    def drag(start_position: tuple, end_position: tuple):
        # Move the mouse to the starting position
        pyautogui.moveTo(start_position)

        # Drag to the ending position
        pyautogui.dragTo(end_position[0], end_position[1], duration=1)


if __name__ == "__main__":
    util = MouseDrag()
    time.sleep(1)
    x, y = MouseMove.get_screen_size()
    util.drag((x // 2, y // 2), (x // 2 - 300, y // 2))
