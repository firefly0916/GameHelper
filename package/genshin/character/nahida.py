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


class Nahida(People):
    def __init__(self):
        name = "nahida"
        super().__init__(name)
        self.cd_e = 6  # duration = 20
        self.cd_q = 13.5
        # self.img_dir = os.path.join(PROJECT_DIR, "package", "genshin", "img")
        # self.e_pic = os.path.join(self.img_dir, "Neuvillette_e.png")

    def monitor(self, action_queue: queue.Queue, exit_flag: bool, is_start_cooldown: dict):
        """
        nahida monitor: 按照设定好的监控级别将行动传入队列
        :return:
        """
        logger_instance.logger.info("Start nahida monitor")

        def a():
            time.sleep(0.5)
            keyboard.press_and_release("2")
            time.sleep(0.5)
            self.super_element_skill()
            time.sleep(0.5)
            self.element_burst()
            return self.name

        while True:
            if not exit_flag:
                while is_start_cooldown[self.name]:
                    action_queue.put(functools.partial(a))
                    logger_instance.logger.info("Adding nahida's element skill to queue")
                    is_start_cooldown[self.name] = False
                    logger_instance.logger.info("start count down nahida's element skill")
                    time.sleep(self.cd_e + 2)  # escape cd is long than gap time
            else:
                logger_instance.logger.info("Exiting nahida's monitor")
                sys.exit()

    def super_element_skill(self):
        time.sleep(0.5)
        keyboard.press("e")
        time.sleep(0.5)
        for i in range(12):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 310, 0, 0, 0)
            time.sleep(0.02)
        keyboard.release("e")
        logger_instance.logger.info(f"{self.name} releases super element skill")


if __name__ == "__main__":
    time.sleep(3)
    nahida = Nahida()
    nahida.super_element_skill()
