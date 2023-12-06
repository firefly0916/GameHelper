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


class Furina(People):
    def __init__(self):
        name = "Furina"
        super().__init__(name)
        self.cd_e = 20  # duration = 30
        self.cd_q = 15
        # self.img_dir = os.path.join(PROJECT_DIR, "package", "genshin", "img")
        # self.e_pic = os.path.join(self.img_dir, "Neuvillette_e.png")

    def monitor(self, action_queue: queue.Queue):
        """
        furina monitor: 按照设定好的监控级别将行动传入队列
        :return:
        """
        logger_instance.logger.info("Start furina monitor")

        def a():
            time.sleep(0.5)
            keyboard.press_and_release("4")
            time.sleep(0.5)
            self.element_skill()
            time.sleep(1)

        while True:
            action_queue.put(functools.partial(a))
            logger_instance.logger.info("Adding furina's element skill to queue")
            time.sleep(28)


if __name__ == "__main__":
    time.sleep(3)
    furina = Furina()
    furina.element_skill()
