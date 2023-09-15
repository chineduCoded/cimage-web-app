import React, { useEffect, useState } from 'react'
import Editor from "@monaco-editor/react";
import "../pages/styles.css"


const CodeEditor = ({ onChange, language, code, theme }) => {
  const [value, setValue] = useState(code || "")
  const [typingTimer, setTypingTimer] = useState(null)

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

  const handleEditorChange = (value) => {
    setValue(value)
    onChange("code", value)
  }


  const calculateTypingTime = (numberOfWords, typingSpeed) => {
    // Calculate the time in seconds to type a certain number of words
    return (numberOfWords / typingSpeed) * 60;
  };

  return (
    <div className="container">
      <Editor
        height="50vh"
        width={`100%`}
        language={language || "python"}
        value={value}
        theme={theme}
        defaultValue="// some comment"
        onChange={handleEditorChange}
        />
    </div>
  );
};

export default CodeEditor;