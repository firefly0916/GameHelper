import functools
import inspect
import os.path
import queue
import sys
import threading
import time

from pathlib import Path

import keyboard
import pyautogui
import pygame
from PIL import Image

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

from package.genshin.character import zhongli, nahida, raiden, furina
from package.logger import SingletonLogger

logger_ins = SingletonLogger()


class HPMonitor(object):
    def __init__(self):
        self.is_stop = False
        self.main_head_thread = threading.Thread(target=self.monitor, daemon=True)
        logger_ins.logger.info("Creat main head Ok")
        pass

    def start(self):
        self.main_head_thread.start()

    def stop(self):
        self.is_stop = True

    def monitor(self):
        current_function_name = inspect.currentframe().f_code.co_name
        region = (820, 1006, 828, 1014)
        while not self.is_stop:
            is_red = self.region_has_red(region=region)
            health = "Health" if not is_red else "Not Health"
            if is_red:
                logger_ins.logger.info("Eating food")
                keyboard.press_and_release('z')
                time.sleep(1)
            logger_ins.logger.info(f"[{current_function_name}] HP: {health}")
            time.sleep(0.5)

        logger_ins.logger.info("HPMonitor stopped")

    @staticmethod
    def region_has_red(region):
        # 截取屏幕上的指定区域
        screenshot = pyautogui.screenshot(region=region)
        pixels = screenshot.load()

        # 检查每个像素是否为红色
        for x in range(screenshot.width):
            for y in range(screenshot.height):
                r, g, b = pixels[x, y]
                if r > 240 and g < 100 and b < 100:
                    return True
        return False


if __name__ == '__main__':
    main_monitor = HPMonitor()
    main_monitor.start()
    time.sleep(10)
    main_monitor.stop()
