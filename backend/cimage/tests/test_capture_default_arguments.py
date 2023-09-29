import mock
from flask import current_app
from cimage.common import capture_screenshoot_url

# Define the test function
def test_capture_screenshot_default_arguments(mocker):
    # Mock the necessary dependencies
    mock_redis_client = mocker.Mock()
    mock_rq = mocker.Mock()
    mock_request = mocker.Mock(args={'url': 'https://example.com'})

    # Mock the enqueue method of rq
    mock_job = mocker.Mock()
    mock_rq.enqueue.return_value = mock_job

    # Mock the result of the job
    mock_job.result.return_value = b'screenshot_bytes'

    # Mock the current_app.config.get method
    mocker.patch('current_app.config.get', return_value='http://localhost')

    # Mock the redis_client and rq attributes of api_bp (if it's defined in your code)
    api_bp = mocker.Mock()
    api_bp.redis_client = mock_redis_client
    api_bp.rq = mock_rq

    # Call the capture_screenshot function
    response = capture_screenshoot_url(mock_request)

    # Assert that the necessary methods were called
    mock_rq.enqueue.assert_called_once_with(capture_screenshoot_url, args=('https://example.com', None))
    mock_job.result.assert_called_once_with(timeout=60)
    mock_redis_client.set_image.assert_called_once_with(mock.ANY, 'c2NyZWVuc2hvdF9ieXRlcw==')

    # Assert the response JSON
    expected_response = {
        'message': 'Screenshot captured successfully',
        'download_url': 'http://localhost/api/v1/download/mock_image_id',
        'image_url': 'http://localhost/api/v1/images/mock_image_id',
        'image_id': mock.ANY,
        'share_link': 'http://localhost/api/v1/share/mock_image_id'
    }
    assert response.json == expected_response
    assert response.status_code == 200
