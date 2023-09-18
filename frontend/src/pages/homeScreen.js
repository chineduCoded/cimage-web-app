import React, { useEffect, useState } from 'react'
import CodeEditor from '../components/DisplayCode'
import { languageOptions } from "../constants/languageOtions"
import { defineTheme } from '../lib/defineTheme'
import ThemeDropdown from '../components/ThemeDropdown'
import LanguagesDropdown from '../components/LanguageDropdown'
import "./styles.css"
import Switcher from '../components/Switcher'
import axios from 'axios'
import DownloadButton from '../components/DownloadButton'


const HomeScreen = () => {
  const [code, setCode] = useState("")
  const [theme, setTheme] = useState("cobalt")
  const [language, setLanguage] = useState(languageOptions[0])
  const [isToggled, setIsToggled] = useState(true)
  const [error, setError] = useState(null);

  const baseURL = "http://localhost:5000"


  useEffect(() => {
    const cancelToken = axios.CancelToken.source()
    axios.get(`${baseURL}/api/v1`, {cancelToken: cancelToken.token})
      .then(res => {
        setCode(res.data)
        console.log(res.data)
      })
      .catch(err => {
        if (axios.isCancel(err)) {
          console.log("Cancelled!")
        } else {
          console.error("Could not fetch code data", err.message)
          setError(`error: ${err.message}`)
        }
      })

      return () => {
        cancelToken.cancel()
      }
  }, [])

  const onSelectChange = (sl) => {
    console.log("selected Option...", sl);
    setLanguage(sl);
  };

  const onChange = (action, data) => {
    switch (action) {
      case "code": {
        setCode(data);
        break;
      }
      default: {
        console.warn("case not handled!", action, data);
      }
    }
  }

  function handleThemeChange(th) {
    const theme = th;
    console.log("theme...", theme);

    if (["light", "vs-dark"].includes(theme.value)) {
      setTheme(theme);
    } else {
      defineTheme(theme.value).then((_) => setTheme(theme));
    }
  }

  useEffect(() => {
    defineTheme("oceanic-next").then((_) =>
      setTheme({ value: "oceanic-next", label: "Oceanic Next" })
    );
  }, []);


  return (
    <main className='home-wrapper'>
        <section className='textarea-wrapper'>
            <CodeEditor
              code={code}
              onChange={onChange}
              language={language?.value}
              theme={theme.value}
            />
        </section>
        <section className='bar'>
            <div className='select-theme common'>
              <h4>Theme</h4>
             <ThemeDropdown handleThemeChange={handleThemeChange} theme={theme} />
            </div>
            <div className='toggle-background common'>
              <h4>Background</h4>
              <Switcher
              rounded={true}
              isToggled={isToggled}
              onToggled={() => setIsToggled(!isToggled)} />
            </div>
            <div className='toggle-dark common'>
              <h4>Dark Mode</h4>
              <Switcher
              rounded={true}
              isToggled={isToggled}
              onToggled={() => setIsToggled(!isToggled)} />
            </div>
            <div className='change-padding common'>
              <h4>Padding</h4>
              <div className='padding-btn'>
                <button>16</button>
                <button>32</button>
                <button>64</button>
                <button>128</button>
              </div>
            </div>
            <div className='select-language common'>
              <h4>language</h4>
              <LanguagesDropdown onSelectChange={onSelectChange} />
            </div>
            <div className='export-screenshot'>
                <DownloadButton />
              <button>up</button>
            </div>
        </section>
    </main>
  )
}

export default HomeScreen