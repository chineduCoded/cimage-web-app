import React from 'react'
import TextArea from '../components/TextArea'
import BelowBar from '../components/BelowBar'
import "./styles.css"

const HomeScreen = () => {
  return (
    <main>
        <section className='textarea'>
            <TextArea />
        </section>
        <section className='bar'>
            <BelowBar />
        </section>
    </main>
  )
}

export default HomeScreen