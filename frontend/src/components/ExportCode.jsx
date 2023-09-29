import { useCallback, useEffect, useState } from 'react'
import { debounce } from "lodash"
import { IoIosArrowUp } from "react-icons/io"
import { ImLink } from "react-icons/im"
import { BsTwitter } from "react-icons/bs"
import "./styles.css"

const ExportCode = () => {
  const [downloadUrl, setDownloadUrl] = useState('');
  const [imageUrl, setImageUrl] = useState('')
  const [shareImageLink, setShareImageLink] = useState('')
  const [imageId, setImageId] = useState('');
  const [dataError, setDataError] = useState(null);
  const [show, setShow] = useState(false)
  // const { image_url, download_url, image_id, share_link } = responseData

  const baseURL = "http://localhost:5000/api/v1"

  // Function to capture the screenshot
  const captureScreenshot = useCallback(async () => {
    try {
        // Make a GET request to your Flask API to capture the screenshot
      const url = "http://localhost:3000"
      const selector = "editor"

      const response = await fetch(`${baseURL}/screenshot?url=${url}&selector=${selector}`)

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }

      const data = await response.json()
        
      if (data) {
        setDownloadUrl(data.download_url);
        setImageUrl(data.image_url)
        setShareImageLink(data.share_link)
        setImageId(data.image_id);
        setDataError(null);
        console.log(data);
      } else {
        console.log("No data available")
      }
    } catch (err) {
      console.error({ error: err });
      setDataError('Screenshot capture failed');
    }
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


  const handleDownload = () => {
    if (downloadUrl) {
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `cimage-${imageId || ''}.png`;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      console.error('Download URL not available');
    }
  };

  const handleCopy = () => {
    if (imageUrl) {
      navigator.clipboard.writeText(imageUrl)
        .then(() => {
          alert('Image URL copied to clipboard');
          console.log('Image URL copied to clipboard');
        })
        .catch(error => console.error('Unable to copy text: ', error));
    } else {
      console.error('Image URL not available');
    }
  };

  const handleShow = () => {
    setShow(!show)
  }

  return (
    <div className='container'>
      <button onClick={handleDownload} className='export'>Export</button>
      {
        show && (
          <div className='share'>
            <div className='share-btns'>
              <div className='btn-wrap'>
                <span className='link'>
                  <ImLink />
                </span>
                <button onClick={handleCopy} className='btn'>Copy URL</button>
              </div>
              <div className='btn-wrap'>
                <span className='tweet'>
                  <BsTwitter />
                </span>
                <button className='btn'>Tweet</button>
              </div>
            </div>
      </div>
        )
      }
        <button onClick={handleShow} className={`show ${show ? 'show-active' : ''}`}>
          <IoIosArrowUp />
        </button>
    </div>
  );
};

export default ExportCode;
