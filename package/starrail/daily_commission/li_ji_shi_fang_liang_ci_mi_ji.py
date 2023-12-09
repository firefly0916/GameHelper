import time
from pathlib import Path
import sys
import os

import cv2
import pyautogui

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

from package.logger import SingletonLogger

logger_ins = SingletonLogger()


class LiJiShiFangLiangCiMiJi(object):
    def __init__(self):
        self.commission_path = os.path.join(PROJECT_DIR, "package", "starrail", "image",
                                            "lei_ji_shi_fang_liang_ci_mi_ji.png")

    def run(self):
        pyautogui.PAUSE = 0.5
        logger_ins.logger.info(f"Start {__file__}")
        logger_ins.logger.info(f"Get commission picture")
        center = pyautogui.locateCenterOnScreen(image=self.commission_path, minSearchTime=1, confidence=0.8)
        pyautogui.leftClick(center.x, center.y)
        logger_ins.logger.info(f"Find commission, continue carrying out")
        # TODO: 这里最好添加一个检测技能点，如果技能点不够2最好采取一些自动行动
        pyautogui.press("esc")
        pyautogui.press("e")
        time.sleep(5)
        pyautogui.press("e")
        time.sleep(5)
        logger_ins.logger.info("Finish carrying out go back commission dashboard")
        pyautogui.press("f4")
        logger_ins.logger.info("Exit current commission")


if __name__ == "__main__":
    com = LiJiShiFangLiangCiMiJi()
    time.sleep(2)
    com.run()
