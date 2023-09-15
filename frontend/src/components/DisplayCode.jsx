import React, { useEffect, useState } from 'react'

import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/ext-language_tools";

import "../pages/styles.css"


const CodeEditor = ({ initialCode }) => {
  const [code, setCode] = useState(initialCode);
  const [typingTimer, setTypingTimer] = useState(null);

  useEffect(() => {
    // Cleanup timer on unmount
    return () => {
      clearTimeout(typingTimer);
    };
  }, [typingTimer]);

//   const handleCodeChange = (e) => {
//     const newCode = e.target.value;
//     setCode(newCode);

//     // Clear the previous timer
//     clearTimeout(typingTimer);

//     // Start a new timer
//     const newTypingTimer = setTimeout(() => {
//       saveCode(newCode);
//     }, 1000); // Adjust the interval as needed

//     setTypingTimer(newTypingTimer);
//   };

  const onChange = (newValue) => {
    console.log("change", newValue)
  }

  const saveCode = (newCode) => {
    // Perform code saving logic here
    // You can make an API request to save the code to your server
    console.log('Code saved:', code);
  };


  const calculateTypingTime = (numberOfWords, typingSpeed) => {
    // Calculate the time in seconds to type a certain number of words
    return (numberOfWords / typingSpeed) * 60;
  };

  return (
    <div>
      <AceEditor
        placeholder="Enter your code here"
        mode="javascript"
        theme="monokai"
        name="blah2"
        // onLoad={onLoad}
        onChange={onChange}
        fontSize={16}
        showPrintMargin={true}
        showGutter={false}
        highlightActiveLine={true}
        value={code}
        setOptions={{
            showLineNumbers: false,
            tabSize: 2,
        }}/>
    </div>
  );
};

export default CodeEditor;