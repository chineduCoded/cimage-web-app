import React, { useEffect, useState } from 'react';
import { usePostScreenshotMutation } from '../services/api';

const DownloadButton = ({ screenshotData }) => {
  // const [imageId, setImageId] = useState('')
  // const [downloalUrl, setDownloadUrl] = useState('')
  // const [imageUrl, setImageUrl] = useState('')

  const { image_url, download_url, image_id } = screenshotData

  
  // const { data: screenshotData, error: screenshotError } = useGetScreenshotQuery({
  //   url: 'http://localhost:3000',
  //   selector: 'editor',
  // });

  // const { data: imageData, error: imageError } = useGetImageIdQuery(imageId || '');

  // useEffect(() => {
  //   if (screenshotError) {
  //     console.error('Error fetching screenshot:', screenshotError);
  //   }
  //   if (imageError) {
  //     console.error('Error fetching image:', imageError);
  //   }
  // }, [screenshotError, imageError]);

  const handleDownload = () => {
    if (download_url) {
      const link = document.createElement('a');
      link.href = download_url;
      link.download = `image-${image_id || ''}.png`;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else {
      console.error('Download URL not available');
    }
  };

  const handleCopy = () => {
    if (image_url) {
      navigator.clipboard.writeText(image_url)
        .then(() => {
          alert('Image URL copied to clipboard');
          console.log('Image URL copied to clipboard');
        })
        .catch(error => console.error('Unable to copy text: ', error));
    } else {
      console.error('Image URL not available');
    }
  };

  return (
    <div>
      <button onClick={handleDownload}>Export</button>
      <button onClick={handleCopy}>Copy URL</button>
    </div>
  );
};

export default DownloadButton;
