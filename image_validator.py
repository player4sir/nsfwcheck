import requests
from io import BytesIO
from PIL import Image
from opennsfw2 import make_open_nsfw_model
from config import Config
import os
import tempfile

# 预加载模型
model = make_open_nsfw_model()

def validate_image(image_data=None, image_url=None):
    temp_file = None
    try:
        if image_data:
            image = Image.open(BytesIO(image_data))
        elif image_url:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        else:
            raise ValueError("Either image_data or image_url must be provided")

        # 验证图像格式
        if image.format.lower() not in Config.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported image format: {image.format}")

        # 转换图像为 RGB 格式
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # 保存到临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        image.save(temp_file.name, 'JPEG')

        # 使用模型进行预测
        nsfw_score = model.predict(temp_file.name)

        is_appropriate = is_image_appropriate(nsfw_score, Config.NSFW_THRESHOLD)

        return {
            'is_appropriate': is_appropriate,
            'nsfw_score': float(nsfw_score),
            'threshold': Config.NSFW_THRESHOLD
        }

    except requests.RequestException as e:
        raise ValueError(f"Error fetching image from URL: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")
    finally:
        if temp_file:
            temp_file.close()
            os.unlink(temp_file.name)

def is_image_appropriate(nsfw_score, threshold):
    return nsfw_score < threshold
