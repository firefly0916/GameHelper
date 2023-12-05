import queue
import sys
import threading
import time

from pathlib import Path

import keyboard

PROJECT_DIR = str(Path(__file__).resolve().parents[3])
sys.path.append(PROJECT_DIR)

from package.genshin.character import neuvillette
from package.logger import SingletonLogger

logger_ins = SingletonLogger()


class ZJNF(object):

    def __init__(self):
        self.act_queue = queue.Queue()

        # 创建任务对象
        na_wei = neuvillette.Neuvillette()
        logger_ins.logger.info("Creat neuvillette Ok")

        # 创建并启动人物监视器线程
        self.na_wei_thread = threading.Thread(target=na_wei.monitor, args=(self.act_queue,), daemon=True)
        self.na_wei_thread.start()
        logger_ins.logger.info("Creat neuvillette monitor Ok")

        # 创建并启动主脑行动线程
        self.main_head_thread = threading.Thread(target=self.main_head, daemon=True)
        self.main_head_thread.start()
        logger_ins.logger.info("Creat main head Ok")

        # 创建并启动热键监听线程
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.hotkey_thread.start()
        logger_ins.logger.info("Create hotkey listener Ok")

    def main_head(self):
        start_time = time.time()
        exit_flag = False
        while not exit_flag:
            try:
                # 从队列中取出可执行函数，非阻塞方式
                executable_function = self.act_queue.get_nowait()

                # 执行函数
                logger_ins.logger.info("Find a action!")
                executable_function()

                # 通知队列任务已经处理完毕
                self.act_queue.task_done()

                # 重置计时器
                start_time = time.time()

            except queue.Empty:
                # 如果队列为空，检查是否超过一分钟
                if time.time() - start_time > 30:
                    # 如果一分钟内没有任务，打印日志并退出循环
                    logger_ins.logger.info("No actions detected for 1 minute. Exiting main_head loop.")
                    exit_flag = True  # 设置标志通知循环退出
                    break

                # 如果队列为空，休眠一小段时间再继续检查
                time.sleep(1)

        # 如果循环退出，执行其他清理操作
        logger_ins.logger.info("Main_head loop exited.")
        exit(0)

    def hotkey_listener(self):
        # 热键监听的逻辑
        keyboard.add_hotkey('ctrl+esc', self.exit_program)
        keyboard.wait('esc')

    def exit_program(self):
        # 退出程序的逻辑
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
    party = ZJNF()
    party.wait_for_threads()
