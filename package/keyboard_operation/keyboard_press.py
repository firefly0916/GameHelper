import time

import keyboard


class Keyboard(object):
    def __init__(self):
        pass

    @staticmethod
    def keyboard_press_and_release(key):
        keyboard.press_and_release(key)

    @staticmethod
    def keyboard_press(key):
        keyboard.press(key)

    @staticmethod
    def keyboard_release(key):
        keyboard.release(key)

    @staticmethod
    def multi_key_press(keys):
        for key in keys:
            Keyboard.keyboard_press(key)

    @staticmethod
    def multi_key_release(keys):
        for key in keys:
            Keyboard.keyboard_release(key)


# Example of using the Keyboard class
if __name__ == "__main__":

    keyboard_instance = Keyboard()
    time.sleep(2)
    keyboard_instance.multi_key_press(["shift", "w"])
    time.sleep(3)
    keyboard_instance.multi_key_release(["shift", "w"])
    time.sleep(0.01)
    keyboard_instance.keyboard_press("w")
    time.sleep(3)
    keyboard_instance.multi_key_release(["w"])
