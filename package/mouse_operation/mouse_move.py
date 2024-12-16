import win32api
import win32con
import win32gui
import time


class MouseMove(object):
    def __init__(self):
        pass

    @staticmethod
    def get_screen_size():
        """

        :return: screen_width, screen_height = MouseMove.get_screen_size()
        """
        hwnd = win32gui.GetDesktopWindow()
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST))
        monitor_rect = monitor_info['Monitor']
        return monitor_rect[2] - monitor_rect[0], monitor_rect[3] - monitor_rect[1]

    @staticmethod
    def set_cursor_to_center():
        screen_width, screen_height = MouseMove.get_screen_size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        win32api.SetCursorPos((center_x, center_y))

    @staticmethod
    def up(distance: int):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -distance, 0, 0)

    @staticmethod
    def down(distance: int):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, distance, 0, 0)

    @staticmethod
    def left(distance: int):

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -distance, 0, 0, 0)

    @staticmethod
    def right(distance: int):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, distance, 0, 0, 0)

    @staticmethod
    def to(x, y):
        win32api.SetCursorPos((x, y))


if __name__ == "__main__":
    main = MouseMove()
    time.sleep(2)
    main.left(2000)
    main.to(1721, 1014)

