import React, { useState, useEffect } from 'react';
import Editor from "@monaco-editor/react";
import "../pages/styles.css";

const CodeEditor = ({ data, language, theme }) => {
  
  const [value, setValue] = useState(data?.code || ""); // Use optional chaining to handle potential undefined values

  const handleChange = (action, data) => {
    switch (action) {
      case "code":
        setValue(data)
        break;
      default:
        console.warn("case not handled!", action, data);
    }
  }
  

  const editorOptions = {
    lineNumbers: "off",
    padding: {
      top: 20,
      bottom: 20
    },
    detectIndentation: true,
    autoIndent: "advanced",
    folding: false,
    tabSize: 4,
    tabCompletion: "on",
    fontFamily: "Inter",
    fontSize: 18,
    scrollbar: {
      vertical: "hidden",
      horizontal: "hidden"
    },
    minimap: {
      enabled: false,
      autohide: true
    },
    // Apply border-radius
    roundedSelection: true,
  }

  // useEffect(() => {
  //   setValue(code?.code || ""); // Update the value when the code prop changes
  // }, [code]);

  return (
    <div className="container">
      <Editor
        height={500}
        language={language || "python"}
        value={value}
        theme={theme}
        defaultValue={data?.code || ""}
        defaultLanguage='python'
        options={editorOptions}
        className='editor'
        loading={null}
        onChange={(value) => handleChange("code", value)}
      />
    </div>
  );
};

export default CodeEditor;
