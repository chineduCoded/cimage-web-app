import React, { useState, useRef, useEffect } from 'react';
import hljs from 'highlight.js';
import 'highlight.js/styles/default.css'; // Import a highlight.js style
// import './CodeEditor.css'; // Import your custom styling

const CustomCodeEditor = ({ initialCode }) => {
  const codeRef = useRef(null);
  const [code, setCode] = useState(initialCode.code);

  console.log(code)

  useEffect(() => {
    // Handle code highlighting when the code state changes
    const highlightedCode = hljs.highlightAuto(code).value;
    codeRef.current.innerHTML = highlightedCode;
  }, [code]);

  const handleCodeChange = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      const { selectionStart, selectionEnd, value } = codeRef.current;
      const startOfLine = value.lastIndexOf('\n', selectionStart - 1) + 1;
      const currentLine = value.substring(startOfLine, selectionStart);
  
      // Determine the appropriate indentation (e.g., 2 spaces per indent)
      const indent = '  '; // You can customize this to your preferred indent style
  
      // Create the new code with the inserted newline and indentation
      const newCode = `${value.substring(0, selectionStart)}\n${indent}${currentLine}${value.substring(selectionEnd)}`;
  
      // Update the code state
      setCode(newCode);
  
      // Move the cursor to the end of the inserted indentation
      codeRef.current.selectionStart = codeRef.current.selectionEnd = selectionStart + indent.length + 1;
    } else {
      // Handle other key presses by updating the code state
      setCode(event.target.value);
    }
  };

  const handleTabKey = (event) => {
    if (event.key === 'Tab') {
      event.preventDefault();
      const { selectionStart, selectionEnd, value } = codeRef.current;
      const startOfLine = value.lastIndexOf('\n', selectionStart - 1) + 1;
      const currentLine = value.substring(startOfLine, selectionStart);
  
      // Determine the appropriate indentation (e.g., 2 spaces per indent)
      const indent = '  '; // You can customize this to your preferred indent style
  
      // Insert the appropriate indentation at the cursor position
      const newCode = `${value.substring(0, selectionStart)}${indent}${value.substring(selectionEnd)}`;
  
      // Update the code state
      setCode(newCode);
  
      // Move the cursor to the end of the inserted indentation
      codeRef.current.selectionStart = codeRef.current.selectionEnd = selectionStart + indent.length;
    }
  };
  
  const handlePaste = (event) => {
    event.preventDefault();
    const pastedCode = event.clipboardData.getData('text/plain');
    const newCode = `${code}${pastedCode}`;
    setCode(newCode);
  };

   

 
  return (
    <div className="code-editor">
      <h1>Code Editor</h1>
    </div>
  );
};

export default CustomCodeEditor;
