import { useEffect, useState } from 'react'
import { languageOptions } from "../constants/languageOtions"
import { defineTheme } from '../lib/defineTheme'
import ThemeDropdown from '../components/ThemeDropdown'
import LanguagesDropdown from '../components/LanguageDropdown'
import "./styles.css"
import Switcher from '../components/Switcher'
import axios from "axios"
import CustomCodeEditor from '../components/CustomCodeEditor'
import ExportCode from '../components/ExportCode'
import { useGetCodeQuery } from '../services/api'


const HomeScreen = () => {
  const [theme, setTheme] = useState("cobalt")
  const [language, setLanguage] = useState(languageOptions[0])
  const [isToggled, setIsToggled] = useState(true)
  // const [error, setError] = useState(null)
  // const [responseData, setResponseData] = useState("")

  const { data: codeData } = useGetCodeQuery()

  const preURL = "http://localhost:3000";
  const preSelector = "editor";
  
  
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

  return (
    <main className='home-wrapper'>
        <section className='textarea-wrapper'>
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
            <div className='select-language common'>
              <h4>language</h4>
              <LanguagesDropdown onSelectChange={onSelectChange} />
            </div>
            <div className='export-screenshot'>
                <ExportCode />
            </div>
        </section>
    </main>
  )
}

export default HomeScreen