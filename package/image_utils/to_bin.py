import cv2
import numpy as np
from PIL import ImageGrab


def highlight_white_areas_with_contrast_enhancement(image_path, alpha=1.5, beta=0):
    # 读取截图
    screenshot = cv2.imread(image_path)

    # 对比度拉伸
    contrast_enhanced_image = np.clip(alpha * screenshot + beta, 0, 255).astype(np.uint8)

    # 使用阈值将图像二值化（将白色部分转换为白色，其他部分转换为黑色）
    _, thresholded_image = cv2.threshold(contrast_enhanced_image, 200, 255, cv2.THRESH_BINARY)

    # 显示处理后的图像
    cv2.imshow("Contrast Enhanced Image", thresholded_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def enhance_custom_golden_tint(image_path, contrast_alpha=1.5, golden_tint=(255, 240, 200)):
    # 读取图像
    original_image = cv2.imread(image_path)

    # 转换图像为浮点数类型
    original_image = original_image.astype(float)

    # 计算颜色通道的缩放比例，以使图像趋近于金黄色
    scale_factors = np.array(golden_tint) / 255.0

    # 缩放图像的各个通道
    enhanced_image = original_image * scale_factors

    # 将图像的蓝色和绿色通道放大，增加整体亮度
    enhanced_image[:, :, 0:2] = enhanced_image[:, :, 0:2] * contrast_alpha

    # 将浮点数类型的图像转换为整型
    enhanced_image = np.clip(enhanced_image, 0, 255).astype(np.uint8)

    # 显示处理后的图像
    cv2.imshow("Enhanced Custom Golden Tint", enhanced_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 你需要提供截图的路径，或者可以使用ImageGrab.grab()获取当前屏幕截图
screenshot_path = 'D:\\git\\GameHelper\\package\\image_utils\\img_1.png'
# screenshot_path = 'temp_screenshot.png'  # 如果你之前保存了截图

# 调用函数进行图像处理和显示
highlight_white_areas_with_contrast_enhancement(screenshot_path)
