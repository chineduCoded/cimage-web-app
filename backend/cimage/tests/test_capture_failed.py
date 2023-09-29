    # Returns an error response with status code 500 if screenshot capture fails
    def test_capture_screenshot_capture_failed(self, mocker):
        # Mock the necessary dependencies
        mock_redis_client = mocker.Mock()
        mock_rq = mocker.Mock()
        mock_request = mocker.Mock(args={'url': 'https://example.com'})

        # Mock the enqueue method of rq
        mock_job = mocker.Mock()
        mock_rq.enqueue.return_value = mock_job

        # Mock the result of the job
        mock_job.result.return_value = None

        # Mock the current_app.config.get method
        mocker.patch('cimage.api.v1.views.api_blueprint.current_app.config.get', return_value='http://localhost')

        # Mock the redis_client and rq attributes of api_bp
        api_bp.redis_client = mock_redis_client
        api_bp.rq = mock_rq

        # Call the capture_screenshot function
        response = capture_screenshot(mock_request)

        # Assert that the necessary methods were called
        mock_rq.enqueue.assert_called_once_with(capture_screenshot_of_url, args=('https://example.com', None))
        mock_job.result.assert_called_once_with(timeout=60)
        mock_redis_client.set_image.assert_not_called()

        # Assert the response JSON
        expected_response = {'error': 'Screenshot capture failed'}
        self.assertEqual(response.json, expected_response)
        self.assertEqual(response.status_code, 500)