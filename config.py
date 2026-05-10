import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB

PREVIEW_MAX_SIZE = 1000  # プレビュー時の長辺最大px

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
UPLOAD_EXPIRE_SECONDS = 1800  # アップロードファイルの保持時間（30分）
