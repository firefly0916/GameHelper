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
        name = "raiden"
        super().__init__(name)
        self.cd_e = 10  # duration = 25
        self.cd_q = 18
        # self.img_dir = os.path.join(PROJECT_DIR, "package", "genshin", "img")
        # self.e_pic = os.path.join(self.img_dir, "Neuvillette_e.png")

    def monitor(self, action_queue: queue.Queue, exit_flag: bool, is_start_cooldown: dict):
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
            return self.name

        while True:
            if not exit_flag:
                logger_instance.logger.info("Adding raiden's element skill to queue")
                while is_start_cooldown[self.name]:
                    action_queue.put(functools.partial(a))
                    is_start_cooldown[self.name] = False
                    logger_instance.logger.info("start count down raiden's element skill")
                    time.sleep(self.cd_e + 2)  # escape cd is long than gap time
            else:
                logger_instance.logger.info("Exiting raiden monitor")
                sys.exit()


if __name__ == "__main__":
    time.sleep(3)
    raiden = Raiden()
    raiden.element_skill()
