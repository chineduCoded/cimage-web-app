import React, { useState } from 'react'
import Editor from "@monaco-editor/react";
import "../pages/styles.css"


const CodeEditor = ({ onChange, language, code, theme }) => {
  const [value, setValue] = useState(code.code || "")

  const handleEditorChange = (value) => {
    setValue(value)
    onChange("code", value)
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

  return (
    <div className="container">
      <Editor
        height={500}
        language={language || "python"}
        value={value}
        theme={theme}
        defaultValue={code.code}
        defaultLanguage='python'
        options={editorOptions}
        className='editor'
        loading={null}
        onChange={handleEditorChange}
        />
    </div>
  );
};

export default CodeEditor;