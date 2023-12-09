import time
import os.path
import sys
from pathlib import Path

import pyautogui

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)
from package.logger import SingletonLogger

logger_ins = SingletonLogger()


class DragCommissionDashboard:
    def __init__(self):
        pass

    @staticmethod
    def drag():
        # 获取屏幕中心坐标
        center_x, center_y = pyautogui.size()[0] // 2, pyautogui.size()[1] // 2

        # 将鼠标移动到屏幕中心
        pyautogui.moveTo(center_x, center_y)

        # 在屏幕中心拖动一定距离（这里需要提供拖动目标的坐标）
        target_x, target_y = center_x - 500, center_y
        pyautogui.dragTo(target_x, target_y, duration=1)  # 可以调整拖动的持续时间
        logger_ins.logger.info("Finish drag screen")


if __name__ == "__main__":
    uti = DragCommissionDashboard()
    time.sleep(1)
    uti.drag()
