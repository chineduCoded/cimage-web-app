import { useState, useEffect } from 'react';
import { api } from '../api/axiosInstance';
import axios from 'axios';
import CodeMirror from '@uiw/react-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { dracula, materialDark, okaidia } from "@uiw/codemirror-themes-all"


const CodeEditor = ({ initialValue }) => {
  const [code, setCode] = useState(initialValue)

  useEffect(() => {
    const cancelToken = axios.CancelToken.source()
    api.get("/api/v1", {cancelToken: cancelToken.token})
      .then(res => {
        // setData(res.data)
        console.log(res.data)
      })
      .catch(err => {
        if (axios.isCancel(err)) {
          console.log("Cancelled!")
        } else {
          console.error("Could not fetch code data", err)
        }
      })

      return () => {
        cancelToken.cancel()
      }
  }, [])

  return (
    <div className='container'>
      <CodeMirror
        value={code}
        height='200px'
        extensions={[javascript({ jsx: true, tsx: true })]}
        theme={okaidia}
        autoFocus={true}
        placeholder="Place your code here"
        className='code-mirror'
      />
    </div>
  );
};

export default CodeEditor;