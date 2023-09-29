import React, { useState, useEffect, useCallback } from 'react';
import { debounce } from 'lodash';
import { useGetCapturedDataQuery } from '../services/api';

function ScreenshotCapture() {
  const [downloadUrl, setDownloadUrl] = useState('');
  const [imageId, setImageId] = useState('');
  const [dataError, setDataError] = useState(null);

  // Function to capture the screenshot
  const captureScreenshot = useCallback(() => {
    // Make a GET request to your Flask API to capture the screenshot
    const url = "http://localhost:3000"
    const selector = "editor"
    fetch(`http://localhost:5000/api/v1/screenshot?url=${url}&selector=${selector}`)
      .then((response) => response.json())
      .then((data) => {
        setDownloadUrl(data.download_url);
        setImageId(data.image_id);
        setDataError(null);
        console.log(data);
      })
      .catch((err) => {
        console.error({ error: err });
        setDataError('Screenshot capture failed');
      });
  }, [])

  const debouncedCaptureScreenshot = useCallback(
    debounce(() => {
      captureScreenshot();
    }, 30000), // Adjust the debounce delay as needed
    []
  );

  // Use useEffect to capture the screenshot automatically
  useEffect(() => {
    debouncedCaptureScreenshot();
  }, [debouncedCaptureScreenshot])

  if (dataError) {
    console.log("error: ", dataError)
  }

  return (
    <div>
      {dataError && <p>Error: {dataError}</p>}
      {downloadUrl && (
        <div>
          <p>Image ID: {imageId}</p>
          <a href={downloadUrl} download>
            Download Screenshot
          </a>
          {/* Display the screenshot image */}
          <img src={downloadUrl} alt="Screenshot" />
        </div>
      )}
    </div>
  );
}

export default ScreenshotCapture;