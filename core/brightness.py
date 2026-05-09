import cv2
import numpy as np


def adjust_brightness_contrast(img, brightness=0, contrast=0):
    """
    brightness: -100 〜 100
    contrast:   -100 〜 100
    """
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha = (highlight - shadow) / 255.0
        gamma = shadow
        img = cv2.addWeighted(img, alpha, img, 0, gamma)

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha = f
        gamma = 127 * (1 - f)
        img = cv2.addWeighted(img, alpha, img, 0, gamma)

    return img
