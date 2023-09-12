import React from 'react'
import { useState } from 'react';

const TextArea = () => {
    const [text, setText] = useState(' How are you doing?');

    const handleInputChange = (e) => {
        setText(e.target.value);
    };
  return (
    <div className='container'>
        <textarea
            className="code"
            rows="20"
            cols="100"
            value={text}
            onChange={handleInputChange}
            placeholder="Enter your text here..."
      >
      </textarea>
    </div>
  )
}

export default TextArea