    # Returns an error response with status code 400 if URL is not provided
    def test_capture_screenshot_no_url(self, mocker):
        # Mock the necessary dependencies
        mock_redis_client = mocker.Mock()
        mock_rq = mocker.Mock()
        mock_request = mocker.Mock(args={})

        # Mock the current_app.config.get method
        mocker.patch('cimage.api.v1.views.api_blueprint.current_app.config.get', return_value='http://localhost')

        # Mock the redis_client and rq attributes of api_bp
        api_bp.redis_client = mock_redis_client
        api_bp.rq = mock_rq

        # Call the capture_screenshot function
        response = capture_screenshot(mock_request)

        # Assert that the necessary methods were not called
        mock_rq.enqueue.assert_not_called()
        mock_redis_client.set_image.assert_not_called()

        # Assert the response JSON
        expected_response = {'error': 'URL is required'}
        self.assertEqual(response.json, expected_response)
        self.assertEqual(response.status_code, 400)