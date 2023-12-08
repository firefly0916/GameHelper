import functools
import queue
import sys
import threading
import time

from pathlib import Path

import keyboard
import pyautogui

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

from package.genshin.character import zhongli, nahida, raiden, furina
from package.logger import SingletonLogger

logger_ins = SingletonLogger()


class God4(object):

    def __init__(self):
        self.act_queue = queue.Queue()
        self.is_start_cooldown = {
            "zhongli": True,
            "nahida": True,
            "raiden": True,
            "furina": True
        }
        self.exit_flag = False

        # 创建并启动主脑行动线程
        def a():
            logger_ins.logger.info("Start domain")
            keyboard.press_and_release("f")
            self.zhongli_thread.start()
            self.nahida_thread.start()
            self.raiden_thread.start()
            self.furina_thread.start()

        self.act_queue.put(functools.partial(a))

        # creat all threads
        self.main_head_thread = threading.Thread(target=self.main_head, daemon=True)
        self.main_head_thread.start()
        logger_ins.logger.info("Creat main head Ok")

        # 创建任务对象
        zhongli_ = zhongli.Zhongli()
        self.zhongli_thread = threading.Thread(target=zhongli_.monitor, args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                               daemon=True)
        logger_ins.logger.info(f"Creat zhongli Ok")
        nahida_ = nahida.Nahida()
        self.nahida_thread = threading.Thread(target=nahida_.monitor, args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                              daemon=True)
        logger_ins.logger.info(f"Creat nahida Ok")
        raiden_ = raiden.Raiden()
        self.raiden_thread = threading.Thread(target=raiden_.monitor, args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                              daemon=True)
        logger_ins.logger.info(f"Creat raiden Ok")
        furina_ = furina.Furina()
        self.furina_thread = threading.Thread(target=furina_.monitor, args=(self.act_queue, self.exit_flag, self.is_start_cooldown),
                                              daemon=True)
        logger_ins.logger.info(f"Creat furina Ok")

        # 创建并启动热键监听线程
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.hotkey_thread.start()
        logger_ins.logger.info("Create hotkey listener Ok")

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
                elif name == "raiden":
                    self.is_start_cooldown["raiden"] = True  # Permit count sown cooldown
                # 通知队列任务已经处理完毕
                self.act_queue.task_done()
            except queue.Empty:
                logger_ins.logger.info("Empty action queue")
                raise Exception("Empty action queue")
            except AttributeError:
                logger_ins.logger.info("Finish listening action queue, now exiting main_head loop.")
                sys.exit("Exiting main_head")

        # 如果循环退出，执行其他清理操作
        logger_ins.logger.info("Main_head loop exited.")
        sys.exit()

    def hotkey_listener(self):
        # 热键监听的逻辑
        keyboard.add_hotkey('ctrl', self.exit_program)
        keyboard.wait('esc')

    def exit_program(self):
        # 退出程序的逻辑
        self.exit_flag = True
        del self.act_queue
        del self.is_start_cooldown
        del self.exit_flag
        logger_ins.logger.info("Exiting program...")
        # 强制退出程序
        sys.exit()

    def wait_for_threads(self):
        # 等待所有线程结束
        self.main_head_thread.join()  # 使用 0 秒超时，立即返回

        # 检查 main_head_thread 是否存活
        if self.main_head_thread.is_alive():
            # 如果线程仍然存活，说明 join 超时，可能需要执行一些额外的操作
            print("main_head_thread is still alive. Additional actions can be performed.")
        else:
            # 如果线程已经结束，可以在这里执行退出操作
            print("main_head_thread has exited. Exiting the program.")
            # 在这里执行其他退出操作，例如关闭资源、清理等
            sys.exit()


if __name__ == "__main__":
    time.sleep(2)
    party = God4()
    party.wait_for_threads()
