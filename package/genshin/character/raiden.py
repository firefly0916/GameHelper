import functools
import os.path
import queue
import sys
import time

from pathlib import Path

import win32api
import win32con

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

import keyboard

from package.logger import SingletonLogger
from package.genshin.character.BasicCharacter import People

logger_instance = SingletonLogger()


class Raiden(People):
    def __init__(self):
        name = "Raiden"
        super().__init__(name)
        self.cd_e = 10  # duration = 25
        self.cd_q = 18
        # self.img_dir = os.path.join(PROJECT_DIR, "package", "genshin", "img")
        # self.e_pic = os.path.join(self.img_dir, "Neuvillette_e.png")

    def monitor(self, action_queue: queue.Queue):
        """
        raiden monitor: 按照设定好的监控级别将行动传入队列
        :return:
        """
        logger_instance.logger.info("Start raiden monitor")

        def a():
            time.sleep(0.5)
            keyboard.press_and_release("3")
            time.sleep(0.5)
            self.element_skill()
            time.sleep(1)

        while True:
            action_queue.put(functools.partial(a))
            logger_instance.logger.info("Adding raiden's element skill to queue")
            time.sleep(23)


if __name__ == "__main__":
    time.sleep(3)
    raiden = Raiden()
    raiden.element_skill()
