import inspect
import os
import random
import sys
import threading
import time
import win32api
import win32con
import win32gui
import keyboard
import pyautogui
import pygame

from package.genshin.PartyOperation import four_archon
from package.logger import SingletonLogger
from package.genshin.character import BasicCharacter
from package.keyboard_operation.keyboard_press import Keyboard
from package.mouse_operation.mouse_move import MouseMove
from package.mouse_operation.mouse_click import MouseClick

logger_ins = SingletonLogger()
mouse_move = MouseMove()
mouse_click = MouseClick()


class Main(object):
    def __init__(self):
        self.party = four_archon.God4()
        self.is_exit = False

    def hot_key_callback(self, event):
        self.is_exit = True
        sys.exit()

    def run_hotkey_listener(self):
        """启动热键监听器的函数"""
        logger_ins.logger.info("Starting hotkey listener...")
        keyboard.add_hotkey('ctrl + shift + a', self.hot_key_callback)
        logger_ins.logger.info("Waiting for hotkey...")
        keyboard.wait()  # 等待热键被按下

    def run(self):
        listener_thread = threading.Thread(target=self.run_hotkey_listener)
        # 启动线程
        listener_thread.start()
        logger_ins.logger.info("Automatically combat start")
        time.sleep(2)
        keyboard.press_and_release("f")  # enter domain
        time.sleep(1)
        while not self.is_exit:
            try:
                click_point = pyautogui.locateCenterOnScreen(
                    image=os.path.join("package", "genshin", "img", "single_start.png"), grayscale=True, confidence=0.7,
                    minSearchTime=1)
                logger_ins.logger.info("Found single start")
                time.sleep(1)
                mouse_move.to(1721, 1014)
                time.sleep(1)
                mouse_move.to(1721, 1014)
                time.sleep(1)
                mouse_click.left_click()
                if click_point is not None:
                    logger_ins.logger.info(click_point)
                    break
            except pyautogui.ImageNotFoundException:
                logger_ins.logger.info("Not found single start")
                time.sleep(0.5)

        # TODO: continue domain main loop
        while True:
            time.sleep(5)
            logger_ins.logger.info("Start domain")
            mouse_click.left_click()
            while True:
                try:
                    box = pyautogui.locateOnScreen(image=os.path.join("package", "genshin", "img", "enter_domain.png"),
                                                   grayscale=True, confidence=0.5)
                    logger_ins.logger.info(f"Box:{box}")
                    logger_ins.logger.info("Found enter domain")
                    time.sleep(1)
                    mouse_click.left_click()
                    break
                except pyautogui.ImageNotFoundException:
                    logger_ins.logger.info("Not found domain")
                    time.sleep(1)

            logger_ins.logger.info("Ready for going straightly and to find start key")
            keyboard.press("w")
            while True:
                try:
                    box = pyautogui.locateOnScreen(image=os.path.join("package", "genshin", "img", "start_key.png"),
                                                   grayscale=False, confidence=0.5, region=(1088, 500, 600, 300))
                    keyboard.release("w")
                    keyboard.press("s")
                    time.sleep(0.1)
                    keyboard.release("s")
                    logger_ins.logger.info(f"Box:{box}")
                    logger_ins.logger.info("Found start key")
                    break
                except pyautogui.ImageNotFoundException:
                    logger_ins.logger.info("Not found start key")
                    time.sleep(0.05)

            time.sleep(1)
            self.party.start()
            self.party.wait_for_threads()
            time.sleep(2)
            logger_ins.logger.info("Automatically combat end")
            logger_ins.logger.info("Going straightly to find direct way to golden tree")
            op_list = ["w", "a", "s", "d"]
            while True:
                key = random.choice(op_list)
                if self.dead_detection(key):
                    logger_ins.logger.info("Found correct way to golden tree")
                    break
                else:
                    keyboard.release(key)
                    keyboard.release("shift")

            logger_ins.logger.info("Ready go straight")
            time.sleep(5)  # 重生加载
            self.detected_reward()
            logger_ins.logger.info("Found receive reward button and stop moving")
            Keyboard.keyboard_press_and_release("f")
            time.sleep(1)
            pyautogui.click(755, 755)  # condemn
            logger_ins.logger.info("Finished this domain")
            time.sleep(12)
            pyautogui.click(1181, 996)
            time.sleep(2)

    def dead_detection(self, key: str):
        dead_image_path = os.path.join("package", "genshin", "img", "dead.png")
        dead_image_dark_path = os.path.join("package", "genshin", "img", "dead_dark.png")
        current_function_name = inspect.currentframe().f_code.co_name
        start_time = time.time()
        keyboard.press("shift")
        keyboard.press(key)
        while True:
            try:
                end_time = time.time()
                diff = end_time - start_time
                if diff >= 10:
                    logger_ins.logger.info("Failed to detected dead")
                    return False
                box = pyautogui.locateOnScreen(dead_image_path, grayscale=True, confidence=0.5)
                keyboard.release(key)
                keyboard.release("shift")
                logger_ins.logger.info(f"Box:{box}")
                logger_ins.logger.info("Successfully detected dead")
                pygame.init()
                pygame.mixer.init()
                sound = pygame.mixer.Sound(
                    os.path.join("package", "genshin", "audio", "detected_dead.wav"))
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))  # 等待音频播放完毕
                return True
            except pyautogui.ImageNotFoundException:
                try:
                    box = pyautogui.locateOnScreen(dead_image_dark_path, grayscale=True, confidence=0.5)
                    keyboard.release(key)
                    keyboard.release("shift")
                    logger_ins.logger.info(f"Box:{box}")
                    logger_ins.logger.info("Successfully detected dead")
                    pygame.init()
                    pygame.mixer.init()
                    sound = pygame.mixer.Sound(
                        os.path.join("package", "genshin", "audio", "detected_dead.wav"))
                    sound.play()
                    pygame.time.wait(int(sound.get_length() * 1000))  # 等待音频播放完毕
                    return True
                except pyautogui.ImageNotFoundException:
                    logger_ins.logger.info(f"[{current_function_name}] image not found")
                    time.sleep(0.1)

    def detected_reward(self):
        challenge_finish_path = os.path.join("package", "genshin", "img", "receive_reward.png")
        current_function_name = inspect.currentframe().f_code.co_name
        keyboard.press("w")
        while True:
            try:
                box = pyautogui.locateOnScreen(challenge_finish_path, grayscale=False, confidence=0.6)
                keyboard.release("w")
                keyboard.press("s")
                time.sleep(0.1)
                keyboard.release("s")
                logger_ins.logger.info(f"Box:{box}")
                try:
                    pygame.init()
                    pygame.mixer.init()
                    sound = pygame.mixer.Sound(
                        os.path.join("package", "genshin", "audio", "detected_reward_button.wav"))
                    sound.play()
                    pygame.time.wait(int(sound.get_length() * 1000))  # 等待音频播放完毕
                except pygame.error as e:
                    print(f"Error playing sound: {e}")
                break
            except pyautogui.ImageNotFoundException:
                logger_ins.logger.info(f"[{current_function_name}] No image found")
                time.sleep(0.05)


if __name__ == '__main__':
    main = Main()
    main.run()
