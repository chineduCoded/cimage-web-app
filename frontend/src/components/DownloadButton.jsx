import React from 'react';
import axios from 'axios';
import { generateUniqueId } from '../lib/generateUniqueId';

const DownloadButton = () => {
  const handleDownloadClick = async () => {
    try {
      const baseUrl = "http://127.0.0.1:5000/api/v1/screenshot/download";
      const params = { url: "http://localhost:3000", selector: "textarea-wrapper" };

      const response = await axios.get(baseUrl, {
        params,
        responseType: 'blob',
      });

      if (response.status === 200) {
        const blob = new Blob([response.data]);
        const contentDisposition = response.headers['content-disposition'];

        // Extract filename from content disposition header
        const match = contentDisposition && contentDisposition.match(/filename="(.+)"/);

        // Generate unique Id to attached when no match
        const filenameId = generateUniqueId()
        console.log(filenameId)

        const filename = match ? match[1] : `cimage-${filenameId}.png`;

        // Create a temporary anchor element to trigger the download
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;

        // Trigger the download
        link.click();

        // Clean up
        window.URL.revokeObjectURL(link.href);
      } else {
        console.error("Image download failed!");
      }
    } catch (error) {
      console.error("Error downloading image:", error.message);
    }
  };

  return (
    <div>
      <button onClick={handleDownloadClick}>Export</button>
    </div>
  );
};

export default DownloadButton;