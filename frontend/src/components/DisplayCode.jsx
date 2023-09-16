import React, { useEffect, useRef, useState } from 'react'
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

  const editorOptions = {
    lineNumbers: "off",
    padding: {
      top: 20,
      bottom: 20
    },
    detectIndentation: true,
    autoIndent: "advanced",
    automaticLayout: true,
    folding: false,
    tabSize: 4,
    tabCompletion: "on",
    fontFamily: "Inter",
    fontSize: 18,
    scrollbar: {
      vertical: "hidden"
    },
    minimap: {
      enabled: false,
      autohide: true
    },
    // Apply border-radius
    roundedSelection: true,
    border: "1px solid #ccc",
    "border-radius": "10px",
  }

  // CSS for the header section
  // const headerCSS = `
  //     .header {
  //         background-color: #333;
  //         color: #fff;
  //         padding: 5px 8px;
  //         display: flex;
  //         align-items: center;
  //     }

  //     .icons {
  //       display: flex;
  //       align-items: center;
  //       justify-content: flex-start;
  //     }

  //     .title {
  //       text-align: center;
  //       display: flex;
  //       justify-content: center;
  //     }
  // `;

  const editorRef = useRef(null)

//   useEffect(() => {
//     if (editorRef.current) {
//         // Access the Monaco Editor instance
//         const monacoEditor = editorRef.current.editor;

//         // Create a custom container element for the header
//         const headerContainer = document.createElement('div');
//         headerContainer.classList.add('editor-header');
//         headerContainer.innerHTML = `
//             <img src="" alt="Editor Icon" />
//             <h3>Code Editor Title</h3>
//         `;

//         // Insert the header container at the top of the editor content
//         monacoEditor.getDomNode().prepend(headerContainer);
//     }
// }, []);

  return (
    <div className="container">
      {/* <style>{headerCSS}</style> */}
      {/* <div className="header">
          <span className='icons'>icon</span>
          <h5 className='title'>{language || "python"}</h5>
      </div> */}
      <Editor
        height="50vh"
        width={`100%`}
        language={language || "python"}
        value={value}
        theme={theme}
        defaultValue="// some comment"
        defaultLanguage='python'
        options={editorOptions}
        className='editor'
        onChange={handleEditorChange}
        // ref={editorRef}
        />
    </div>
  );
};

export default CodeEditor;