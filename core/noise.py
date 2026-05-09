import cv2
import numpy as np


def apply_noise_reduction(img, strength=0):
    """
    strength: 0 〜 100
    fastNlMeansDenoisingColored でノイズを除去する
    """
    if strength == 0:
        return img

    h = int(3 + (strength / 100.0) * 17)  # 3 〜 20
    return cv2.fastNlMeansDenoisingColored(img, None, h, h, 7, 21)
