import sys
from pathlib import Path

import pyautogui

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))
import time
import numpy as np
import win32api
import win32con

from package.image_utils import compare
from package.mouse_operation.mouse_move import MouseMove


class MouseClick(object):
    def __init__(self):
        pass

    @staticmethod
    def left_click():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    @staticmethod
    def right_click():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    @staticmethod
    def left_click_matched_image(screenshot: np.ndarray, sub_image: np.ndarray):
        top_left, bottom_right = compare.ImageCompare.get_sub_image_pos(screen_image=screenshot,
                                                                        template_image=sub_image)
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        MouseMove.to(center[0], center[1])
        MouseClick.left_click()


# Example of using the MouseClick class
if __name__ == "__main__":
    mouse_click = MouseClick()

    time.sleep(2)
    # Left click
    mouse_click.left_click()
