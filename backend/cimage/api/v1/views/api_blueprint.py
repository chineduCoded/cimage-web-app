#!/usr/bin/python3
"""API Blueprint"""
from flask import jsonify, session, request, current_app
from cimage.api.v1.views import api_bp
import bleach
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles


PLACEHOLDER_CODE = "print('Hello, World!')"
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
        return jsonify({"error": f"error: {str(e)}"}), 500



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
        return jsonify({"error": str(e)}), 500