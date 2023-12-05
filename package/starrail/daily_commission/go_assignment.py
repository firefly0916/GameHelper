import os.path
import sys
from pathlib import Path
PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)
import time
import cv2
import keyboard

from package.image_utils.compare import ImageCompare
from package.mouse_operation.mouse_click import MouseClick
from package.mouse_operation.mouse_move import MouseMove
from package.config import set_logger


class GoAssignment(object):
    def __init__(self):
        self.commission_path = os.path.join(PROJECT_DIR, "package", "starrail", "image", "go_assignment.png")

    def run(self):
        # TODO: Check integrate
        # TODO: 本过程并未添加复杂的图片检测，所有过程都是粗略计时，需要将派遣设置为专属材料的前四个，可以提issue去实现
        # TODO: 简易开发，能用固定位置，不用cv， 能用绝对position不用相对position
        logger = set_logger()

        logger.info("Get commission picture...")
        commission = cv2.imread(self.commission_path)

        logger.info("Checking matched picture")
        top_left, bottom_right = ImageCompare.circle_check(commission, logger)

        logger.info("Calculating center")
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        # click going button
        MouseMove.to(center[0], center[1] + 170)
        MouseClick.left_click()
        time.sleep(1)

        for i in range(4):
            # 点击领取 1480， 900
            MouseMove.to(1480, 900)
            MouseClick.left_click()
            time.sleep(1)
            # 再次派遣 1200， 950
            MouseMove.to(1200, 950)
            MouseClick.left_click()
            # 这里出现一个等待
            time.sleep(5)

        keyboard.press_and_release("esc")
        logger.info("Finish this commission!")


if __name__ == "__main__":
    pass
