from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import base64
from io import BytesIO
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Get the Base64 image from the request
        data = request.get_json()
        print("Request Data:", data)
        image_data = data.get('image')

        if not image_data:
            return jsonify({"error": "No image provided"}), 400

        # Fix any potential incorrect padding in Base64 string
        image_data = image_data + '=' * (4 - len(image_data) % 4)  # Ensure correct padding

        # Decode the Base64 image
        try:
            img_bytes = base64.b64decode(image_data)
            print("Decoded image bytes length:", len(img_bytes))
        except Exception:
            return jsonify({"error": "Failed to decode Base64 image"}), 400

        # Validate that the image can be opened by PIL
        try:
            with Image.open(BytesIO(img_bytes)) as img:
                img.verify()  # Verify it's a valid image
        except Exception:
            return jsonify({"error": "Invalid image format"}), 400

        # Remove the background
        try:
            output = remove(img_bytes)
        except Exception as e:
            return jsonify({"error": f"Error in background removal: {str(e)}"}), 500

        # Convert the processed image to Base64
        processed_image = base64.b64encode(output).decode('utf-8')

        return jsonify({
            "message": "Background removed successfully",
            "processed_image": processed_image
        })

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
