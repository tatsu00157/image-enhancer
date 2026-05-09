import cv2
import numpy as np


def apply_sharpness(img, strength=0):
    """
    strength: 0 〜 100
    アンシャープマスクで輪郭を強調する
    """
    if strength == 0:
        return img

    sigma = 3.0
    amount = strength / 100.0 * 2.0  # 最大2.0倍

    img_float = img.astype(np.float32)
    blurred = cv2.GaussianBlur(img_float, (0, 0), sigma)
    sharpened = img_float + amount * (img_float - blurred)
    return np.clip(sharpened, 0, 255).astype(np.uint8)
