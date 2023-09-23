import React, { useState, useEffect, useMemo } from "react";
import CodeEditor from "@uiw/react-textarea-code-editor";
import rehypePrism from "rehype-prism-plus";
import { debounce } from "lodash";
import { useSaveCodeMutation } from "../services/api";

const initialCode = `
    def get_file_type(binary_data):
      file_types = {
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'\xFF\xD8\xFF': 'JPEG',
        b'GIF87a': 'GIF',
        b'GIF89a': 'GIF',
        b'\x42\x4D': 'BMP',  # BMP file signature
        // Add more file signatures and corresponding file types as needed
      }

      for signature, file_type in file_types.items():
        if binary_data.startswith(signature):
          return file_type

      return 'Unknown';
    `;

const CustomCodeEditor = ({ data }) => {
  const [codeValue, setCodeValue] = useState("");
  const [saveCode, {isLoading, isError, error}] = useSaveCodeMutation()

  useEffect(() => {
    setCodeValue(data?.code || "");
  }, [data]);

  // Memoize the debouncedSaveCode function using useMemo
  const debouncedSaveCode = useMemo(() => {
    return debounce((codeToSave) => {
      const res = saveCode(codeToSave); // Trigger the mutation with the codeToSave

      if (res) {
        console.log("Code saved successfully")
      } else {
        console.error("Code saving failed")
      }
    }, 2000);
  }, [saveCode]);

  useEffect(() => {
    debouncedSaveCode(codeValue);
  }, [codeValue, debouncedSaveCode]);

  return (
    <CodeEditor
      value={codeValue}
      defaultValue={initialCode}
      onChange={(e) => setCodeValue(e.target.value)}
      placeholder="Paste your code"
      padding={15}
      language="python"
      data-color-mode="dark"
      rehypePlugins={[[rehypePrism, { ignoreMissing: true }]]}
      className="editor"
      cols={data?.max_chars}
      rows={data?.num_lines}
      minHeight={200}
      style={{
        fontSize: 16,
        // backgroundColor: "#f5f5f5",
        borderRadius: 15,
        minWidth: 520,
        fontFamily:
          'ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace',
      }}
    />
  );
};

export default CustomCodeEditor;