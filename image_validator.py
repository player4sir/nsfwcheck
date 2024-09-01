import requests
from io import BytesIO
from PIL import Image
from opennsfw2 import predict_image
from config import Config
import os
import tempfile

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

        # Validate image format
        if image.format.lower() not in Config.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported image format: {image.format}")

        # Convert image to RGB if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Save to a temporary file if needed by opennsfw2
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        image.save(temp_file.name, 'JPEG')
        
        nsfw_score = predict_image(temp_file.name)
        is_appropriate = is_image_appropriate(nsfw_score, Config.NSFW_THRESHOLD)
        
        result = {
            'is_appropriate': is_appropriate,
            'nsfw_score': float(nsfw_score),
            'threshold': Config.NSFW_THRESHOLD
        }

        return result

    except requests.RequestException as e:
        raise ValueError(f"Error fetching image from URL: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")
    finally:
        # Clean up
        if temp_file:
            temp_file.close()
            os.unlink(temp_file.name)
        
        # Explicitly delete objects to free memory
        if 'image' in locals():
            del image
        if 'image_data' in locals():
            del image_data
        if 'response' in locals():
            del response

def is_image_appropriate(nsfw_score, threshold):
    return nsfw_score < threshold
