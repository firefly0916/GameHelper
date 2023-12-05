import sys
import time
from pathlib import Path

import pyautogui

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)
import keyboard
from package.logger import SingletonLogger

logger_instance = SingletonLogger()


class People(object):
    def __init__(self, name: str):
        self.name = name

    def move(self, key: str):
        """
        Control people moving
        :param key: ["w","a","d","s"]
        :return:
        """
        keyboard.press(key)
        logger_instance.logger.info(f"{self.name} is moving -- {key}")

    def shift_move(self, key: str):
        """
        Control people shift move
        :param key:
        :return:
        """
        keyboard.press("shift")
        keyboard.press(key)
        logger_instance.logger.info(f"{self.name} is fast moving -- {key}")

    def stop(self, key: str):
        """
        Control people stop moving
        :param key: ["w","a","d","s"]
        :return:
        """
        keyboard.release(key)
        logger_instance.logger.info(f"{self.name} stops moving -- {key}")

    def shift_stop(self, key: str):
        """
        Control people stop moving
        :param key: ["w","a","d","s"]
        :return:
        """
        keyboard.release("shift")
        keyboard.release(key)
        logger_instance.logger.info(f"{self.name} stops fast moving -- {key}")

    def element_skill(self):
        keyboard.press_and_release("e")
        logger_instance.logger.info(f"{self.name} releases element skill")

    def element_burst(self):
        keyboard.press_and_release("q")
        logger_instance.logger.info(f"{self.name} releases element burst")


if __name__ == "__main__":
    time.sleep(3)
    peo = People("Neuvillette")
    peo.move("w")
    time.sleep(3)
    peo.stop("w")
    time.sleep(1)
    peo.element_skill()
