import React, { useState, useEffect } from 'react';

function CodeEditor() {
  const [code, setCode] = useState('');
  const [typingTimeout, setTypingTimeout] = useState(null);

  const handleCodeChange = (event) => {
    const newCode = event.target.value;
    setCode(newCode);

    // Calculate the time to type a certain number of words
    const numberOfWords = 100; // Replace with your desired number of words
    const typingSpeed = 50; // Replace with your typing speed in words per minute
    const timeInSeconds = calculateTypingTime(numberOfWords, typingSpeed);

    // Clear the previous typingTimeout
    clearTimeout(typingTimeout);

    // Set a new typingTimeout after typing stops
    const delay = timeInSeconds * 1000; // Convert time to milliseconds
    const newTypingTimeout = setTimeout(() => {
      saveCodeToBackend(newCode);
    }, delay);

    setTypingTimeout(newTypingTimeout);
  };

  const calculateTypingTime = (numberOfWords, typingSpeed) => {
    // Calculate the time in seconds to type a certain number of words
    return (numberOfWords / typingSpeed) * 60;
  };

  const saveCodeToBackend = (newCode) => {
    // Perform code-saving logic here
    // You can make an API request to save the code to your server
    console.log('Code saved to backend:', newCode);

    // Example API request (replace with your actual API request)
    // fetch('/api/save-code', {
    //   method: 'POST',
    //   body: JSON.stringify({ code: newCode }),
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    // })
    //   .then((response) => {
    //     if (!response.ok) {
    //       throw new Error(`HTTP error! Status: ${response.status}`);
    //     }
    //     return response.json();
    //   })
    //   .then((data) => {
    //     console.log('Backend response:', data);
    //     // Handle the response from the backend here
    //   })
    //   .catch((error) => {
    //     console.error('Error:', error);
    //     // Handle any errors that occurred during the fetch
    //   });
  };

  return (
    <div>
      <textarea
        value={code}
        onInput={handleCodeChange}
        placeholder="Enter your code..."
      />
      {/* Render other components here */}
    </div>
  );
}

export default CodeEditor;
