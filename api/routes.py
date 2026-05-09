import os
import uuid
import cv2
import numpy as np
from flask import Blueprint, request, jsonify, send_from_directory, render_template, send_file
import config
from core.brightness import adjust_brightness_contrast
from core.color import adjust_white_balance
from core.sharpen import apply_sharpness
from core.noise import apply_noise_reduction
from core.shadow import apply_shadow_correction

api_bp = Blueprint("api", __name__)


def allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in config.ALLOWED_EXTENSIONS


def load_image(filename):
    path = os.path.join(config.UPLOAD_FOLDER, filename)
    img = cv2.imread(path)
    if img is None:
        return None
    return img


def resize_for_preview(img):
    h, w = img.shape[:2]
    max_size = config.PREVIEW_MAX_SIZE
    if max(h, w) <= max_size:
        return img
    scale = max_size / max(h, w)
    return cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)


def encode_to_jpeg(img):
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return buf.tobytes()


def apply_transforms(img, data):
    rotation = int(data.get("rotation", 0))
    flip_h = data.get("flip_h", False)
    flip_v = data.get("flip_v", False)

    if rotation == 90:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif rotation == 180:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif rotation == 270:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    if flip_h:
        img = cv2.flip(img, 1)
    if flip_v:
        img = cv2.flip(img, 0)

    return img


@api_bp.route("/")
def index():
    return render_template("index.html")


@api_bp.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "ファイルがありません"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "ファイルが選択されていません"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "対応していないファイル形式です（jpg/jpeg/png/webp のみ）"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(config.UPLOAD_FOLDER, filename)
    file.save(save_path)

    return jsonify({"filename": filename})


@api_bp.route("/api/preview", methods=["POST"])
def preview():
    data = request.get_json()
    if not data or "filename" not in data:
        return jsonify({"error": "filenameが必要です"}), 400

    img = load_image(data["filename"])
    if img is None:
        return jsonify({"error": "画像が見つかりません"}), 404

    img = resize_for_preview(img)

    brightness = int(data.get("brightness", 0))
    contrast = int(data.get("contrast", 0))
    white_balance = data.get("white_balance", "none")
    sharpness = int(data.get("sharpness", 0))
    noise_reduction = int(data.get("noise_reduction", 0))
    shadow_correction = int(data.get("shadow_correction", 0))

    img = apply_transforms(img, data)
    img = adjust_brightness_contrast(img, brightness, contrast)
    img = adjust_white_balance(img, white_balance)
    img = apply_shadow_correction(img, shadow_correction)
    img = apply_noise_reduction(img, noise_reduction)
    img = apply_sharpness(img, sharpness)

    preview_filename = f"preview_{data['filename'].split('.')[0]}.jpg"
    preview_path = os.path.join(config.UPLOAD_FOLDER, preview_filename)
    cv2.imwrite(preview_path, img)

    return jsonify({"preview_filename": preview_filename})


@api_bp.route("/api/download", methods=["POST"])
def download():
    data = request.get_json()
    if not data or "filename" not in data:
        return jsonify({"error": "filenameが必要です"}), 400

    img = load_image(data["filename"])
    if img is None:
        return jsonify({"error": "画像が見つかりません"}), 404

    brightness = int(data.get("brightness", 0))
    contrast = int(data.get("contrast", 0))
    white_balance = data.get("white_balance", "none")
    sharpness = int(data.get("sharpness", 0))
    noise_reduction = int(data.get("noise_reduction", 0))
    shadow_correction = int(data.get("shadow_correction", 0))

    img = apply_transforms(img, data)
    img = adjust_brightness_contrast(img, brightness, contrast)
    img = adjust_white_balance(img, white_balance)
    img = apply_shadow_correction(img, shadow_correction)
    img = apply_noise_reduction(img, noise_reduction)
    img = apply_sharpness(img, sharpness)

    fmt = data.get("format", "jpg").lower()
    if fmt not in ("jpg", "png"):
        fmt = "jpg"

    download_filename = f"download_{data['filename'].split('.')[0]}.{fmt}"
    download_path = os.path.join(config.UPLOAD_FOLDER, download_filename)

    if fmt == "png":
        cv2.imwrite(download_path, img)
    else:
        cv2.imwrite(download_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])

    return send_file(download_path, as_attachment=True, download_name=f"enhanced.{fmt}")


@api_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(config.UPLOAD_FOLDER, filename)
