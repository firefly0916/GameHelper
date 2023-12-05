import cv2
import mss
import numpy as np
from PIL import ImageGrab


class ScreenShoot(object):
    def __init__(self):
        pass

    @staticmethod
    def get_screen_shoot() -> np.ndarray:
        # Get the screen size
        screen_size = ImageGrab.grab().size

        # Get the screen shot using ImageGrab.grab()
        screenshot = np.array(ImageGrab.grab(bbox=(0, 0, screen_size[0], screen_size[1])))

        return screenshot

    @staticmethod
    def get_screen_shoot_area(screen_area: tuple) -> np.ndarray:
        # Get the screen shot using ImageGrab.grab() with the specified area
        screenshot = np.array(ImageGrab.grab(bbox=(screen_area[0], screen_area[1], screen_area[2], screen_area[3])))

        return screenshot


# Example of using the get_screen_shoot function
if __name__ == "__main__":
    # Create a ScreenShoot object
    screen_shooter = ScreenShoot()

    # Get the screen shot
    screenshot = screen_shooter.get_screen_shoot()

    # Display the screen shot
    cv2.imshow('Screen Shot', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
