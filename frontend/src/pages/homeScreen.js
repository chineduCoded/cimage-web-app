import React from 'react'
import BelowBar from '../components/BelowBar'
import "./styles.css"
import CodeEditor from '../components/DisplayCode'

const HomeScreen = () => {
  const initialCode = `function greet(name) {
    return "Hello, " + name + "!";
  }`;
  
  return (
    <main>
        <section className='textarea-wrapper'>
            <CodeEditor initialCode={initialCode} />
        </section>
        <section className='bar'>
            <BelowBar />
        </section>
    </main>
  )
}

export default HomeScreen