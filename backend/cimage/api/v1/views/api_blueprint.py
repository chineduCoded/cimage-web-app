#!/usr/bin/python3
"""API Blueprint"""
import time
import uuid
from io import BytesIO
import base64
import asyncio
import json
from cachetools import LRUCache
from cachetools.keys import hashkey
from flask import jsonify, session, request, current_app, send_file
from cimage.api.v1.views import api_bp
import bleach
import tweepy
from cimage.common.capture_screenshoot_url import capture_screenshot_of_url
from cimage.common.generate_unique_session_id import generate_unique_session_id
from cimage.common.has_correct_padding import has_correct_padding
from config import Config
from playwright.async_api import async_playwright

cache = LRUCache(maxsize=100)



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
            return jsonify({"error": "Code not found in Redis"}), 404

        code = code_bytes.decode("utf-8")  # Decode from bytes to string
        lines = code.split("\n")

        response_data = {
            "message": "successful",
            "display": "Code retrieved from Redis",
            "code": code,
            "num_lines": len(lines),
            "max_chars": len(max(lines, key=len)),
        }

        return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"error: {str(e)}")
        return jsonify({"error": "Internal Server Error: Unable to fetch code"}), 500



@api_bp.route("/save-code", methods=["POST"])
def save_code():
    try:
        redis_client = api_bp.redis_client

        # Decode the bytes to a text string
        code_bytes = request.get_data()
        code = code_bytes.decode("utf-8")

        # sanitized_code = bleach.clean(code, tags=[], attributes={}, strip=True)

        if not code:
            current_app.logger.error("No code provided")
            return jsonify({"error": "No code provided"}), 400
        
        if len(code) > 10000:
            current_app.logger.error("Code is too long!")
            return jsonify({"error": "Code is too long!"}), 400
        
        redis_client.set("code", code)

        current_app.logger.info("Code saved successfully")

        return jsonify({
            "message": "Code saved successfully",
            "session_id": session.sid
        }), 201

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
    """Captures screenshot of web page using css selector"""
    try:
        redis_client = api_bp.redis_client

        # Get the URL and page locator from the query parameters
        url = request.args.get("url")
        page_locator = request.args.get("selector")

        # Check if URL is provided
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        try:
            screenshot_bytes = asyncio.run(capture_screenshot_of_url(url, page_locator))


            if not screenshot_bytes:
                return {'error': 'Page not available!'}, 404
            
            
            try:
                # Encode the image data as a base64-encoded string
                screenshot_base64 = base64.b64encode(screenshot_bytes).decode()

            except Exception as e:
                # Handle the encoding error here
                print(f"Error encoding screenshot bytes to base64: {str(e)}")
                return jsonify({'error': f'Error encoding screenshot: {str(e)}'}), 500


            # Generate a unique identifier for the image
            image_id = uuid.uuid4()

            # Store the image data in the Redis session
            redis_client.set_image(image_id, screenshot_base64)

            base_url = current_app.config.get("BASE_URL")
            image_url = f"{base_url}/api/v1/images/{image_id}"
            download_url = f"{base_url}/api/v1/download/{image_id}"

            response_data = {
                'message': 'Screenshot captured successfully',
                'image_id': image_id,
                'image_url': image_url,
                'download_url': download_url
            }

            return jsonify(response_data), 200

        except Exception as e:
            current_app.logger.error(f"Error capturing screenshot: {str(e)}")
            return {'error': f'Error capturing screenshot: {str(e)}'}, 500

    except Exception as e:
        error_message = f'Internal Server Error: {str(e)}'
        current_app.logger.error(f"Error handling screenshot request: {error_message}")
        return jsonify({'error': error_message}), 500



        
@api_bp.route('/download/<image_id>', methods=['GET', 'POST'])
def download_image(image_id):
    try:
        redis_client = api_bp.redis_client

        # Retrieve the image data from the Redis session
        image_data_base64 = redis_client.get_image(image_id)

        if image_data_base64 is None:
            return jsonify({'error': 'Image not found'}), 404

        try:
            # Decode the base64-encoded image data back into binary data
            image_data = base64.b64decode(image_data_base64)
        except Exception as decode_error:
            current_app.logger.error(f"Base64 decoding error: {str(decode_error)}")
            return jsonify({'error': f'Base64 decoding error: {str(decode_error)}'}), 500

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
    """
    Capture and download a screenshot of a given URL.

    :return:
        If successful, returns the screenshot as a downloadable file with 
        the image ID and download URL in the response JSON.
        If there is an error, returns an error response with 
        the appropriate status code and error message.
    """
    try:
        redis_client = api_bp.redis_client

        # Get the URL to capture from the request
        url = request.args.get('url')
        
        # Get the page locator from the request
        page_locator = request.args.get('selector')

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

        # Set the 'content-disposition' header to specify the filename
        filename = f'cimage_{image_id}.png'
       
        return  send_file(image_stream, mimetype='image/png', as_attachment=True, download_name=filename)

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
            
        try:
            # Decode the base64-encoded image data back into binary data
            image_data = base64.b64decode(image_data_base64)
        except Exception as decode_error:
            current_app.logger.error(f"Base64 decoding error: {str(decode_error)}")
            return jsonify({'error': f'Base64 decoding error: {str(decode_error)}'}), 500

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
        base_url = "http://localhost:5000"
        image_url = f"{base_url}/api/v1/images/{image_id}"

        return jsonify({'image_url': image_url}), 200

    except Exception as e:
        current_app.logger.error(f"Error downloading image: {str(e)}")
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500
    

@api_bp.route("/share/<image_id>", methods=["POST"])
def share_to_twitter(image_id):
    """Share screenshot to twitter"""
    try:
        redis_client = api_bp.redis_client

        image_data_base64 = redis_client.get_image(image_id)

        if image_data_base64 is None:
            return jsonify({"Error": "Image not found"}), 404
        image_data = base64.b64decode(image_data_base64)

        if not image_data:
            return jsonify({"error": "Empty image data"}), 500
        
        image_stream = BytesIO(image_data)

        # Access Twitter API credentials from the configuration
        consumer_key = Config.TWITTER_CONSUMER_KEY
        consumer_secret = Config.TWITTER_CONSUMER_SECRET
        access_token = Config.TWITTER_ACCESS_TOKEN
        access_token_secret = Config.TWITTER_ACCESS_TOKEN_SECRET

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        # Compose a tweet
        tweet_text = request.json.get("tweet_text")

        if tweet_text is None:
            return jsonify({"error": "Tweet text is required"}), 400

        # Upload to Twitter
        media = api.media_upload(filename=f"cimage_{image_id}.png", file=image_stream)
        api.update_status(status=tweet_text, media_ids=[media.media_id])

        return jsonify({"message": "Screenshot share to Twitter successfully"}), 200

    except Exception as e:
        current_app.logger.error(f"Error sharing image to twitter: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
   
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
