import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB

PREVIEW_MAX_SIZE = 1000  # プレビュー時の長辺最大px
