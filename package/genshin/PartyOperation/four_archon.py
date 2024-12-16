import functools
import inspect
import os.path
import queue
import sys
import threading
import time

from pathlib import Path

import keyboard
import pyautogui
import pygame

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

from package.genshin.character import zhongli, nahida, raiden, furina, hp_monitor
from package.logger import SingletonLogger

logger_ins = SingletonLogger()


class God4(object):

    def __init__(self):
        self.finish_thread: threading.Thread
        self.furina_thread: threading.Thread
        self.raiden_thread: threading.Thread
        self.nahida_thread: threading.Thread
        self.zhongli_thread: threading.Thread
        self.hp_monitor_thread: threading.Thread
        self.main_head_thread: threading.Thread
        self.act_queue = queue.Queue()
        self.is_start_cooldown = {
            "zhongli": True,
            "nahida": True,
            "raiden": True,
            "furina": True
        }
        self.exit_flag = False
        self._create_threads()

    def _create_threads(self):

        # 创建并启动主脑行动线程
        def a():
            logger_ins.logger.info("Start domain")
            keyboard.press_and_release("f")

        self.act_queue.put(functools.partial(a))

        # creat all threads
        self.main_head_thread = threading.Thread(target=self.main_head, daemon=True)
        logger_ins.logger.info("Creat main head Ok")

        # 创建任务对象
        zhongli_ = zhongli.Zhongli()
        self.zhongli_thread = threading.Thread(target=zhongli_.monitor,
                                               args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                               daemon=True)
        logger_ins.logger.info(f"Creat zhongli Ok")
        nahida_ = nahida.Nahida()
        self.nahida_thread = threading.Thread(target=nahida_.monitor,
                                              args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                              daemon=True)
        logger_ins.logger.info(f"Creat nahida Ok")
        raiden_ = raiden.Raiden()
        self.raiden_thread = threading.Thread(target=raiden_.monitor,
                                              args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                              daemon=True)
        logger_ins.logger.info(f"Creat raiden Ok")
        furina_ = furina.Furina()
        self.furina_thread = threading.Thread(target=furina_.monitor,
                                              args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                              daemon=True)
        logger_ins.logger.info(f"Creat furina Ok")
        hp_ = hp_monitor.HPMonitor()
        self.hp_thread = threading.Thread(target=hp_.monitor, daemon=True)
        logger_ins.logger.info(f"Creat hp monitor Ok")

        # 创建finish monitor
        self.finish_thread = threading.Thread(target=self.challenge_finish_monitor, daemon=True)
        logger_ins.logger.info("Create finish monitor listener Ok")

    def start(self):
        self.main_head_thread.start()
        self.zhongli_thread.start()
        self.nahida_thread.start()
        self.raiden_thread.start()
        self.furina_thread.start()
        self.hp_thread.start()
        self.finish_thread.start()

    def main_head(self):
        logger_ins.logger.info("Start listening action queue")
        while not self.exit_flag:
            try:
                # 从队列中取出可执行函数，非阻塞方式
                executable_function = self.act_queue.get()
                # 执行函数
                logger_ins.logger.info("Find a action!")
                name = executable_function()
                if name == "zhongli":
                    self.is_start_cooldown["zhongli"] = True  # Permit count sown cooldown
                elif name == "nahida":
                    self.is_start_cooldown["nahida"] = True  # Permit count sown cooldown
                elif name == "raiden":
                    self.is_start_cooldown["raiden"] = True  # Permit count sown cooldown
                elif name == "furina":
                    self.is_start_cooldown["furina"] = True  # Permit count sown cooldown
                # 通知队列任务已经处理完毕
                self.act_queue.task_done()
            except queue.Empty:
                logger_ins.logger.info("Empty action queue")
                raise Exception("Empty action queue")
            except AttributeError:
                logger_ins.logger.info("Finish listening action queue, now exiting main_head loop.")

        # 如果循环退出，执行其他清理操作
        logger_ins.logger.info("Main_head loop exited.")
        del self.hp_thread
        del self.zhongli_thread
        del self.nahida_thread
        del self.raiden_thread
        del self.furina_thread

    def wait_for_threads(self):
        # 等待所有线程结束
        self.main_head_thread.join()  # 使用 0 秒超时，立即返回

        # 检查 main_head_thread 是否存活
        if self.main_head_thread.is_alive():
            # 如果线程仍然存活，说明 join 超时，可能需要执行一些额外的操作
            logger_ins.logger.info("main_head_thread is still alive. Additional actions can be performed.")
        else:
            # 如果线程已经结束，可以在这里执行退出操作
            logger_ins.logger.info("main_head_thread has exited. Exiting the program.")
            # 在这里执行其他退出操作，例如关闭资源、清理等

    def challenge_finish_monitor(self):
        challenge_finish_path = os.path.join(PROJECT_DIR, "package", "genshin", "img", "challenge_finish_bin.png")
        current_function_name = inspect.currentframe().f_code.co_name
        while True:
            try:
                box = pyautogui.locateOnScreen(challenge_finish_path, grayscale=False, confidence=0.4)
                logger_ins.logger.info(f"Box:{box}")
                try:
                    pygame.init()
                    pygame.mixer.init()
                    sound = pygame.mixer.Sound(os.path.join(PROJECT_DIR, "package", "genshin", "audio", "challenging_finished.wav"))
                    sound.play()
                    pygame.time.wait(int(sound.get_length() * 1000))  # 等待音频播放完毕
                except pygame.error as e:
                    print(f"Error playing sound: {e}")
                self.exit_program()
                break
            except pyautogui.ImageNotFoundException:
                logger_ins.logger.info(f"[{current_function_name}] No image found")
                time.sleep(0.5)

    def exit_program(self):
        # 退出程序的逻辑
        self.exit_flag = True
        del self.act_queue
        del self.is_start_cooldown
        logger_ins.logger.info("Exiting program...")
        # 强制退出程序


if __name__ == "__main__":
    time.sleep(2)
    party = God4()
    party.start()
    party.wait_for_threads()
    print("I can do other actions")
