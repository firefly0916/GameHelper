import functools
import os.path
import queue
import sys
import time

from pathlib import Path

import cv2
import pyautogui
import win32api
import win32con

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

from package.logger import SingletonLogger
from package.genshin.character.BasicCharacter import People
from package.image_utils.compare import ImageCompare

logger_instance = SingletonLogger()


class Neuvillette(People):
    def __init__(self):
        name = "Neuvillette"
        super().__init__(name)
        self.cd_e = 12
        self.cd_q = 18
        self.img_dir = os.path.join(PROJECT_DIR, "package", "genshin", "img")
        self.e_pic = os.path.join(self.img_dir, "Neuvillette_e.png")

    def monitor(self, action_queue: queue.Queue):
        """
        neuvillette monitor: 按照设定好的监控级别将行动传入队列
        :return:
        """
        e_pic = cv2.imread(self.e_pic)
        while True:
            logger_instance.logger.info("Checking Neuvillette element skill is available")
            screen_area = (1600, 950, 1919, 1079)
            ImageCompare.circle_check(e_pic, threshold=0.7)
            logger_instance.logger.info("Neuvillette element skill is available", (1600, 950, 1919, 1079))
            action_queue.put(functools.partial(self.element_skill))
            logger_instance.logger.info("Add Neuvillette element skill to queue")
            time.sleep(1)
            action_queue.put(functools.partial(self.rotate))
            logger_instance.logger.info("Add Neuvillette rotate burst to queue")

    def rotate(self):
        w, h = pyautogui.size()
        logger_instance.logger.info(f"{self.name} is rotating")
        start_time = time.time()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        # TODO: 命中敌人是转4秒，如果e未命中以后再说
        while time.time() - start_time < 4:
            win32api.SetCursorPos((w // 2, h // 2))
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 300, 0, 0, 0)
            # 设置循环间隔
            time.sleep(0.01)

        # 模拟鼠标左键释放
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        logger_instance.logger.info(f"{self.name} stops rotating")


if __name__ == "__main__":
    time.sleep(3)
    Neuvi = Neuvillette()
