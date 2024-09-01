from flask import Flask, request, jsonify
from image_validator import validate_image
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config.from_object(Config)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/validate', methods=['POST'])
@limiter.limit("10 per minute")
def validate():
    try:
        if 'image' in request.files:
            image_file = request.files['image']
            image_data = image_file.read()
            result = validate_image(image_data=image_data)
        elif 'url' in request.json:
            image_url = request.json['url']
            result = validate_image(image_url=image_url)
        else:
            return jsonify({'error': 'No image or URL provided'}), 400

        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error processing request'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
