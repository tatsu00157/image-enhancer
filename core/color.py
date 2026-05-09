import cv2
import numpy as np


def adjust_white_balance(img, mode="none"):
    """
    mode: "none" | "auto" | "daylight" | "fluorescent" | "incandescent"
    """
    if mode == "none":
        return img

    if mode == "auto":
        result = img.copy().astype(np.float32)
        avg_b = np.mean(result[:, :, 0])
        avg_g = np.mean(result[:, :, 1])
        avg_r = np.mean(result[:, :, 2])
        avg_gray = (avg_b + avg_g + avg_r) / 3
        result[:, :, 0] = np.clip(result[:, :, 0] * (avg_gray / avg_b), 0, 255)
        result[:, :, 1] = np.clip(result[:, :, 1] * (avg_gray / avg_g), 0, 255)
        result[:, :, 2] = np.clip(result[:, :, 2] * (avg_gray / avg_r), 0, 255)
        return result.astype(np.uint8)

    # プリセット（BGR順）
    presets = {
        "daylight":      (1.0,  1.0,  1.0),
        "fluorescent":   (1.1,  1.0,  0.85),
        "incandescent":  (0.85, 1.0,  1.2),
    }
    gains = presets.get(mode, (1.0, 1.0, 1.0))
    result = img.copy().astype(np.float32)
    for ch, gain in enumerate(gains):
        result[:, :, ch] = np.clip(result[:, :, ch] * gain, 0, 255)
    return result.astype(np.uint8)
