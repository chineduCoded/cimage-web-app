#!/usr/bin/python3
"""API Blueprint"""
import uuid
from io import BytesIO
import base64
import asyncio
import json
from flask import jsonify, session, request, current_app, send_file, Response
from cimage.api.v1.views import api_bp
import bleach
from cimage.common.capture_screenshoot_url import capture_screenshot_of_url
from cimage.common.generate_unique_session_id import generate_unique_session_id



PLACEHOLDER_CODE = """
@app.route("/")
def index():
    \"\"\"Home page\"\"\"
    context = {
        "page_title": "API Home",
        "current_year": datetime.now().year
    }
    return render_template("home.html", **context)
"""
DEFAULT_STYLE = "dracula"


@api_bp.route("/", methods=["GET"])
def code():
    """Get the codes"""
    try:
        redis_client = api_bp.redis_client

        # Try to get code from Redis
        code_bytes = redis_client.get("code")

        if code_bytes is None:
            sanitized_code = bleach.clean(PLACEHOLDER_CODE, tags=[], attributes={}, strip=True)
            sanitized_code_bytes = sanitized_code.encode("utf-8")  # Encode as bytes
            redis_client.set("code", sanitized_code_bytes)
            code_bytes = sanitized_code_bytes

        code = code_bytes.decode("utf-8")  # Decode from bytes to string
        lines = code.split("\n")

        response_data = {
            "message": "successful",
            "display": "Paste your code",
            "code": code,
            "num_lines": len(lines),
            "max_chars": len(max(lines, key=len)),
        }

        return jsonify(response_data), 200
    
    except Exception as e:
        current_app.logger.error(f"error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500



@api_bp.route("/save_code", methods=["POST"])
def save_code():
    try:
        redis_client = api_bp.redis_client

        # Decode the bytes to a text string
        code_bytes = request.get_data()
        code = code_bytes.decode("utf-8")

        sanitized_code = bleach.clean(code, tags=[], attributes={}, strip=True)

        if not sanitized_code:
            current_app.logger.error("No code provided")
            return jsonify({"error": "No code provided"}), 400
        
        if len(sanitized_code) > 1500:
            current_app.logger.error("Code is too long!")
            return jsonify({"error": "Code is too long!"}), 400
        
        redis_client.set("code", sanitized_code)

        current_app.logger.info("Code saved successfully")

        return jsonify({"message": "Code saved successfully", "session_id": session.sid}), 201

    except Exception as e:
        current_app.logger.error(f"error: {str(e)}")
        
        return jsonify({"error": "Internal Server Error"}), 500

@api_bp.route("/reset", methods=["POST"])
def clear_code():
    try:
        redis_client = api_bp.redis_client

        if redis_client.get("code"):
            redis_client.clear("code")

            sanitized_code = bleach.clean(PLACEHOLDER_CODE, tags=[], attributes={}, strip=True)
            sanitized_code_bytes = sanitized_code.encode("utf-8")  # Encode as bytes
            redis_client.set("code", sanitized_code_bytes)

            return jsonify({"message": "Session cleared successfully"}), 200
        else:
            return jsonify({"message": "Session does not exist"}), 404

    except Exception as e:
        current_app.logger.error(f"Error clearing session: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@api_bp.route("/screenshot", methods=["GET"])
def capture_screenshot():
    try:
        redis_client = api_bp.redis_client

        # Get the URL to capture from the request
        url = request.host_url
        
        # Get the page locator from the request
        page_locator = request.form.get('locator')

        # Check if URL is provided
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Use asyncio to run the Playwright code
        screenshot_bytes = asyncio.run(capture_screenshot_of_url(url, page_locator))

        if not screenshot_bytes:
            return jsonify({'error': 'Screenshot capture failed'}), 500
        
        # Encode the image data as a base64-encoded string
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode()

        # Generate a unique identifier for the image
        image_id = generate_unique_session_id()

        # Store the image data in the Redis session
        # image_data = open(screenshot_bytes, 'rb').read()
        redis_client.set("image_id", screenshot_base64)

        # Generate a URL for downloading the image
        download_url = f"/api/v1/download/{image_id}"

        return jsonify({'download_url': download_url, "image_id": image_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@api_bp.route('/download/<image_id>', methods=['GET', 'POST'])
def download_image(image_id):
    redis_client = api_bp.redis_client

    # Retrieve the image data from the Redis session
    image_data_base64 = redis_client.get("image_id")

    if not image_data_base64:
        return jsonify({'error': 'Image not found'}), 404
    
    # Decode the base64-encoded image data back into binary data
    image_data = base64.b64decode(image_data_base64)

    # Create a BytesIO stream from the image data
    image_stream = BytesIO(image_data)

    # Return the image as a downloadable file
    return send_file(image_stream, mimetype='image/png', as_attachment=True, download_name=f'cimage_{image_id}.png')

@api_bp.route('/screenshot/download', methods=['GET'])
def capture_and_download_screenshot():
    try:
        redis_client = api_bp.redis_client

        # Get the URL to capture from the request
        url = request.host_url
        
        # Get the page locator from the request
        page_locator = request.form.get('locator')

        # Check if URL is provided
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Use asyncio to run the Playwright code
        screenshot_bytes = asyncio.run(capture_screenshot_of_url(url, page_locator))

        if not screenshot_bytes:
            return jsonify({'error': 'Screenshot capture failed'}), 500

        # Encode the image data as a base64-encoded string
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode()

        # Generate a unique identifier for the image
        image_id = generate_unique_session_id()

        # Store the image data in the Redis session
        redis_client.set("image_id", screenshot_base64)

        # Create a BytesIO stream from the image data
        image_stream = BytesIO(screenshot_bytes)

        # Return the image as a downloadable file
        return send_file(image_stream, mimetype='image/png', as_attachment=True, download_name=f'cimage_{image_id}.png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api_bp.route('/delete', methods=['DELETE'])
def delete_image():
    redis_client = api_bp.redis_client

    # Try to get image data from the Redis session
    image_data = redis_client.get("image_id")

    if not image_data:
        return jsonify({'error': 'Image not found'}), 404
    
    # Delete the image data from the Redis session
    deleted_count = redis_client.delete("image_id")

    if deleted_count == 0:
        return jsonify({'error': 'Image not found'}), 404

    return '', 204

@api_bp.route('/images', methods=['GET'])
def get_all_images():
    redis_client = api_bp.redis_client
    
    # Get image data using the key
    images_data = redis_client.get('image_id')

    if images_data:
        response = Response(images_data, content_type='image/png')
        return response
    else:
        return jsonify({'error': 'Images not found'}), 404

@api_bp.route('/images/<image_id>', methods=['GET'])
def get_single_image(image_id):
    redis_client = api_bp.redis_client

    # Get image data using the key
    images_data = redis_client.get('image_id')

    if images_data:
        response = Response(images_data, content_type='image/png')
        return response
    
    return jsonify({'error': 'Image not found'}), 404
