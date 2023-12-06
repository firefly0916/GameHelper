import functools
import os.path
import queue
import sys
import time

from pathlib import Path

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

import keyboard

from package.logger import SingletonLogger
from package.genshin.character.BasicCharacter import People

logger_instance = SingletonLogger()


class Zhongli(People):
    def __init__(self):
        name = "Zhongli"
        super().__init__(name)
        self.cd_e = 12  # duration = 20
        self.cd_q = 12
        # self.img_dir = os.path.join(PROJECT_DIR, "package", "genshin", "img")
        # self.e_pic = os.path.join(self.img_dir, "Neuvillette_e.png")

    def monitor(self, action_queue: queue.Queue):
        """
        zhongli monitor: 按照设定好的监控级别将行动传入队列
        :return:
        """
        logger_instance.logger.info("Start zhongli monitor")

        def a():
            time.sleep(0.5)
            keyboard.press_and_release("1")
            time.sleep(1)
            self.super_element_skill()
            time.sleep(1)

        while True:
            time.sleep(13)
            action_queue.put(functools.partial(a))
            logger_instance.logger.info("Adding zhongli's element skill to queue")


    def super_element_skill(self):
        keyboard.press("e")
        time.sleep(1)
        keyboard.release("e")
        time.sleep(0.5)
        logger_instance.logger.info(f"{self.name} releases super element skill")


if __name__ == "__main__":
    time.sleep(3)
    zhongli = Zhongli()
    zhongli.super_element_skill()
