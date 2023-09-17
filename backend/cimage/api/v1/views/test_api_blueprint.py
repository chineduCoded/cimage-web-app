
# Generated by CodiumAI
from flask import app
from backend.cimage.api.v1.views.api_blueprint import capture_and_download_screenshot


import pytest

class TestCaptureAndDownloadScreenshot:

    # Returns a downloadable screenshot file with a unique name and image ID.
    def test_download_screenshot_with_unique_name_and_id(self):
        # Mock the request object
        with app.test_request_context('/screenshot/download?url=http://example.com&locator=body'):
            # Call the capture_and_download_screenshot function
            response = capture_and_download_screenshot()

            # Check the response status code
            assert response.status_code == 200

            # Check the response content type
            assert response.headers['Content-Type'] == 'image/png'

            # Check the response content disposition
            assert response.headers['Content-Disposition'] == 'attachment; filename=cimage_{image_id}.png'

            # Check if the image ID is present in the response JSON
            assert 'image_id' in response.json

            # Check if the download URL is present in the response JSON
            assert 'download_url' in response.json

