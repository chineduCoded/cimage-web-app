import React, { useEffect, useState } from 'react'
import CodeEditor from '../components/DisplayCode'
import { languageOptions } from "../constants/languageOtions"
import { defineTheme } from '../lib/defineTheme'
import ThemeDropdown from '../components/ThemeDropdown'
import LanguagesDropdown from '../components/LanguageDropdown'
import "./styles.css"
import Switcher from '../components/Switcher'
import DownloadButton from '../components/DownloadButton'
import { useGetCodeQuery, useGetScreenshotQuery } from '../services/api'
import axios from "axios"
import CustomCodeEditor from '../components/CustomCodeEditor'


const HomeScreen = () => {
  const [theme, setTheme] = useState("cobalt")
  const [language, setLanguage] = useState(languageOptions[0])
  const [isToggled, setIsToggled] = useState(true)
  const [error, setError] = useState(null)
  const [screenshotData, setScreenshotData] = useState("")

  const { data: codeData } = useGetCodeQuery();
  // const { data: captured } = useGetScreenshotQuery({
  //   url: "http://localhost:3000",
  //   selector: "editor"
  // })

  // useEffect(() => {
  //   const cancelToken = axios.CancelToken.source()
  //   const baseURL = "http://localhost:5000/api/v1"
  //   const preURL = "http://localhost:3000"
  //   const selector = "editor"
  //   const fetchData = async () => {

  //     try {
  //       const res = await axios.get(`${baseURL}/capture?url=${preURL}&selector=${selector}`, {cancelToken: cancelToken.token})

  //       const data = res.data

  //       if (data) {
  //         console.log(data)
  //       } else {
  //         console.error("Couldn't fetch data")
  //       }
  //     } catch (error) {
  //       if (axios.isCancel(error)) {
  //         console.log("Request cancelled:", error.message)
  //       } else {
  //         console.error("An error occurred:", error)
  //       }
  //     }
  //   }

  //   fetchData()

  //   return () => {
  //     cancelToken.cancel("Request canceled due to component unmount");
  //   }
  // }, [])

  const onSelectChange = (sl) => {
    console.log("selected Option...", sl);
    setLanguage(sl);
  };

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

  // useEffect(() => {
  //   const handleScreenshot = async () => {
  //     try {
  //       const res = await postScreenshot({
  //         url: "http://localhost:3000",
  //         selector: "editor"
  //       })

  //       const data = res.data
  //       if (data) {
  //         console.log(data)
  //         setScreenshotData(data)
  //       }
  //     } catch (err) {
  //       console.error("error", err.message)
  //     }
  //   }

  //   if (!screenshotData) {
  //     handleScreenshot()
  //   }
  // }, [])

  return (
    <main className='home-wrapper'>
        <section className='textarea-wrapper'>
            {/* <CodeEditor
              data={codeData}
              language={language?.value}
              theme={theme.value}
            /> */}
            <CustomCodeEditor data={codeData} />
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
                <DownloadButton screenshotData={screenshotData} />
              <button>up</button>
            </div>
        </section>
    </main>
  )
}

export default HomeScreen