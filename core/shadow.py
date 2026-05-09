import cv2
import numpy as np


def apply_shadow_correction(img, strength=0):
    """
    strength: 0 〜 100
    CLAHEで暗部・影を持ち上げてコントラストを均等化する
    """
    if strength == 0:
        return img

    clip_limit = 1.0 + (strength / 100.0) * 3.0  # 1.0 〜 4.0

    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l)

    lab_enhanced = cv2.merge([l_enhanced, a, b])
    return cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
