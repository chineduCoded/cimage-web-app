#!/usr/bin/python3
"""API Blueprint"""
import uuid
from io import BytesIO
import base64
import asyncio
import json
from flask import jsonify, session, request, current_app, send_file, make_response
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
    """Get the code from Redis or set a default code."""
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
        return jsonify({"error": "Internal Server Error: Unable to fetch code"}), 500



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
        redis_client.set_image(image_id, screenshot_base64)


        # Generate a URL for downloading the image
        download_url = f"/api/v1/download/{image_id}"

        return jsonify({'message': 'Screenshot captured successfully', 'download_url': download_url, 'image_id': image_id})

    except Exception as e:
        current_app.logger.error(f"Error capturing screenshot: {str(e)}")
        jsonify({'error': f'Internal Server Error: {str(e)}'}), 500
    
    
@api_bp.route('/download/<image_id>', methods=['GET', 'POST'])
def download_image(image_id):
    try:
        redis_client = api_bp.redis_client

        # Retrieve the image data from the Redis session
        image_data_base64 = redis_client.get_image(image_id)

        if image_data_base64 is None:
            return jsonify({'error': 'Image not found'}), 404
        
        # Decode the base64-encoded image data back into binary data
        image_data = base64.b64decode(image_data_base64)

        if not image_data:
            return jsonify({'error': 'Empty image data'}), 500

        # Create a BytesIO stream from the image data
        image_stream = BytesIO(image_data)

        # Return the image as a downloadable file
        return send_file(image_stream, mimetype='image/png', as_attachment=True, download_name=f'cimage_{image_id}.png')

    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

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
        redis_client.set_image(image_id, screenshot_base64)

        # Create a BytesIO stream from the image data
        image_stream = BytesIO(screenshot_bytes)

        # Return the image as a downloadable file
        return send_file(image_stream, mimetype='image/png', as_attachment=True, download_name=f'cimage_{image_id}.png')

    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500
    
@api_bp.route('/delete', methods=['DELETE'])
def delete_all_images():
    try:
        redis_client = api_bp.redis_client

        # Delete all images from the Redis session
        redis_client.clear_all_images()

        return '', 204

    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500
    
@api_bp.route('/delete/<image_id>', methods=['DELETE'])
def delete_single_image(image_id):
    try:
        redis_client = api_bp.redis_client

        # Try to get image data from the Redis session using the provided image_id
        image_data = redis_client.get_image(image_id)

        if not image_data:
            return jsonify({'error': 'Image not found'}), 404
        
        # Delete the image data from the Redis session
        redis_client.delete_image(image_id)

        return '', 204
    
    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

@api_bp.route('/images', methods=['GET'])
def get_all_images():
    try:
        redis_client = api_bp.redis_client

        # Get all images from the Redis session
        all_images = redis_client.get_all_images()

        if all_images:
            # Return a list of image data
            image_list = [{'image_id': image_id, 'image_data': image_data.decode('utf-8')} for image_id, image_data in all_images.items()]
            return jsonify(image_list)
        else:
            return jsonify({'error': 'Images not found'}), 404

    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500


@api_bp.route('/images/<image_id>', methods=['GET'])
def get_single_image(image_id):
    try:
        redis_client = api_bp.redis_client

        # Get image data using the provided image_id
        image_data_base64 = redis_client.get_image(image_id)
        

        if image_data_base64 is None:
            return jsonify({'error': 'Image not found'}), 404
            
        # Decode the base64-encoded image data back into binary data
        image_data = base64.b64decode(image_data_base64)

        if not image_data:
            return jsonify({'error': 'Empty image data'}), 500

        # Create a BytesIO stream from the image data
        image_stream = BytesIO(image_data)

        return send_file(image_stream, mimetype='image/png', download_name=f'cimage_{image_id}.png')

    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500



@api_bp.route('/copy/<image_id>', methods=['GET'])
def copy_image_address(image_id):
    try:
        redis_client = api_bp.redis_client

        # Check if the image with the provided image_id exists
        if not redis_client.exists(f"image:{image_id}"):
            return jsonify({'error': 'Image not found'}), 404

        # Define the URL for accessing the image based on the provided image_id
        image_url = f"/api/v1/images/{image_id}"

        return jsonify({'image_url': image_url}), 200

    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500
   
@api_bp.route('/clear', methods=['POST'])
def clear_all_images():
    try:
        redis_client = api_bp.redis_client

        # Call the custom method to clear all images
        redis_client.clear_all_images()

        return '', 204  # Successfully cleared all images

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404  # No images found in the session

    except Exception as e:
        current_app.logger.error(f"Error clearing all images: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500
