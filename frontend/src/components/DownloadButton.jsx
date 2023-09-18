import React from 'react';
import axios from 'axios';
// import { generateUniqueId } from '../lib/generateUniqueId';

const DownloadButton = () => {

  const handleDownload = async () => {
    try {
        // Capture the screenshot and get the image_id
        const baseUrl = "http://127.0.0.1:5000";
        const params = { url: "http://localhost:3000", selector: "editor" };

        const response = await axios.get(`${baseUrl}/api/v1/screenshot`, {
          params,
        });

        if (response.status === 200) {
          const { image_id } = response.data;

          if (image_id) {
            // Construct the download URL using the image_id
            const downloadUrl = `${baseUrl}/api/v1/download/${image_id}`;

            // Create an anchor element and set its href to the download URL
            const link = document.createElement("a");
            link.href = downloadUrl;
            link.download = `cimage-${image_id}.png`;

            // Add the link element to the document's body
            document.body.appendChild(link);

            link.click();

            // Remove the link element from the DOM after download
            document.body.removeChild(link);
          } else {
          console.error("Invalid image_id received!");
          }
        } else {
          console.error("Image capture failed!", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error.message);
    }
  };

  return (
    <div>
      <button onClick={handleDownload}>
        Export
      </button>
    </div>
  );
};

export default DownloadButton;
