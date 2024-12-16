import pyautogui
import cv2
import numpy as np

# 获取屏幕截图
screenshot = pyautogui.screenshot()
frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# 显示截图
cv2.imshow("Screenshot", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
