import os

class Config:
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 16 MB
    NSFW_THRESHOLD = float(os.environ.get('NSFW_THRESHOLD', '0.5'))
