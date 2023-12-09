import os.path
import threading
import time
import pyautogui
import win32api
import win32con
from PIL import ImageGrab


def find_exit_gate():
    img_path = "D:\\git\\GameHelper\\package\\genshin\\img\\exit_gate1.png"
    while True:
        try:
            box = pyautogui.locateOnScreen(img_path, grayscale=True, confidence=0.5)
            print("Box:", box)
            break
        except pyautogui.ImageNotFoundException:
            print("not found")
            time.sleep(1)


def capture_and_save_screenshot(i):
    file_name = f"D:\\git\\GameHelper\\package\\image_utils\\screenshot\\screenshot_{i}.png"
    ImageGrab.grab().save(file_name)


def get_screen_shoot_circuit():
    threads = []
    for i in range(12):
        thread = threading.Thread(target=capture_and_save_screenshot, args=(i,))
        threads.append(thread)
        thread.start()
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 310, 0, 0, 0)
        time.sleep(0.3)

    # 等待所有线程结束
    for thread in threads:
        thread.join()


# 调用函数
if __name__ == '__main__':
    time.sleep(2)
    pyautogui.keyDown("e")
    time.sleep(0.5)
    get_screen_shoot_circuit()
    pyautogui.keyUp("e")
