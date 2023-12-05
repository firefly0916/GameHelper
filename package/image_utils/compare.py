import logging
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[2]))

from package.image_utils.screen_shoot import ScreenShoot
from package.logger import SingletonLogger
logger_ins = SingletonLogger()
import cv2
import numpy as np


class ImageCompare(object):
    def __init__(self):
        pass

    @staticmethod
    def get_sub_image_pos(screen_image: np.ndarray, template_image: np.ndarray, threshold=0.8):
        # 转换图像为灰度
        screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

        # 使用模板匹配方法（TM_CCO-EFF_NORMED）
        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        # 获取最大匹配值和位置
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # 如果匹配值超过阈值，则认为匹配成功
        if max_val >= threshold:
            # 获取子图在全屏截图中的位置
            h, w = template_gray.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            return top_left, bottom_right
        else:
            # 如果匹配值未达到阈值，返回 None 表示未成功匹配
            return None

    @staticmethod
    def circle_check(sub_image: np.ndarray, threshold=0.8, duration=1.5, screen_area=None):
        """
        循环截屏检查
        :param duration: 循环间断时间
        :param threshold: 模糊度
        :param sub_image: 子图
        :param screen_area: 截图区域，格式为 (x1, y1, x2, y2) 或 None（全屏）
        :return: result [tuple: (top_left, bottom_right)]
        """
        while True:
            # 获取截图
            if screen_area:
                screen_image = ScreenShoot.get_screen_shoot_area(screen_area)
            else:
                screen_image = ScreenShoot.get_screen_shoot()

            logger_ins.logger.info("Get screenshot...")
            result = ImageCompare.get_sub_image_pos(screen_image, sub_image, threshold)
            logger_ins.logger.info("Get match info...")

            if result:
                logger_ins.logger.info("Match found. Stop looping")
                top_left, bottom_right = result
                logger_ins.logger.info(f"Top Left Corner:{str(top_left)}")
                logger_ins.logger.info(f"Bottom Right Corner:{str(bottom_right)}")
                return result
            else:
                logger_ins.logger.info("No match found. Go looping...")
                time.sleep(duration)


if __name__ == "__main__":
    pass
