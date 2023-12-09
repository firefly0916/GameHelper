import os
import sys
import time
from pathlib import Path

import pyautogui

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

from package.logger import SingletonLogger

logger_ins = SingletonLogger()


class TakeAPicture:
    def __init__(self):
        self.commission_path = os.path.join(PROJECT_DIR, "package", "starrail", "image", "take_a_picture.png")

    def run(self):
        logger_ins.logger.info("Starting take_a_picture")
        logger_ins.logger.info("Find matched commission")
        center = pyautogui.locateCenterOnScreen(image=self.commission_path, minSearchTime=1, confidence=0.8)
        if center is not None:
            logger_ins.logger.info("Find matched commission")
            pyautogui.leftClick(center.x, center.y)
            pyautogui.press("esc")
            time.sleep(2)
            pyautogui.press("esc")
            time.sleep(2)
            pyautogui.leftClick(1870, 575)
            time.sleep(2)
            pyautogui.press("f")
            time.sleep(2)
            pyautogui.press("esc")
            time.sleep(2)
            pyautogui.press("esc")
            time.sleep(2)
            pyautogui.press("f4")
            time.sleep(1)
            logger_ins.logger.info(f"Finish carrying out current take_a_picture {__file__}")
        else:
            raise Exception("No commission found")


if __name__ == "__main__":
    take = TakeAPicture()
    time.sleep(1)
    take.run()
