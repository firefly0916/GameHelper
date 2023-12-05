import os.path
import sys
from pathlib import Path
PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)
import time
import cv2
import keyboard

from package.image_utils.compare import ImageCompare
from package.image_utils.screen_shoot import ScreenShoot
from package.mouse_operation.mouse_click import MouseClick
from package.mouse_operation.mouse_move import MouseMove
from package.config import set_logger


class HeChengYiCiCaiLiao(object):
    def __init__(self):
        self.commission_path = os.path.join(PROJECT_DIR, "package", "starrail", "image", "he_cheng_yi_ci_cai_liao.png")
        self.button_he_cheng = os.path.join(PROJECT_DIR, "package", "starrail", "image", "button_he_cheng.png")
        self.button_confirm = os.path.join(PROJECT_DIR, "package", "starrail", "image", "button_confirm.png")

    def run(self):
        # TODO: Check integrate
        logger = set_logger()

        logger.info("Get commission picture...")
        commission = cv2.imread(self.commission_path)

        logger.info("Checking matched picture")
        top_left, bottom_right = ImageCompare.circle_check(commission, logger)

        logger.info("Calculating center")
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        MouseMove.to(center[0], center[1] + 170)
        MouseClick.left_click()
        time.sleep(1)

        logger.info("Get button_he_cheng picture...")
        button_he_cheng = cv2.imread(self.button_he_cheng)
        logger.info("Checking matched picture...")
        if ImageCompare.circle_check(button_he_cheng, logger):
            screen_image = ScreenShoot().get_screen_shoot()
            MouseClick.left_click_matched_image(screen_image, button_he_cheng)

        logger.info("Get button_confirm picture...")
        button_confirm = cv2.imread(self.button_confirm)
        logger.info("Checking confirm button...")
        if ImageCompare.circle_check(button_confirm, logger):
            screen_image = ScreenShoot().get_screen_shoot()
            MouseClick.left_click_matched_image(screen_image, button_confirm)

        time.sleep(1.5)
        MouseClick.left_click()
        time.sleep(1.5)
        keyboard.press_and_release("esc")
        logger.info("Finish this daily commission successfully!")


if __name__ == "__main__":
    pass
