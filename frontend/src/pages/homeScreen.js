import React, { useEffect, useState } from 'react'
import CodeEditor from '../components/DisplayCode'
import { languageOptions } from "../constants/languageOtions"
import { defineTheme } from '../lib/defineTheme'
import "./styles.css"
import ThemeDropdown from '../components/ThemeDropdown'
import LanguagesDropdown from '../components/LanguageDropdown'

const initialCode = `function greet(name) {
  return "Hello, " + name + "!";
}`;

const HomeScreen = () => {
  const [code, setCode] = useState(initialCode)
  const [theme, setTheme] = useState("cobalt")
  const [language, setLanguage] = useState(languageOptions[0])

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
    <main>
        <section className='textarea-wrapper'>
            <CodeEditor
              code={code}
              onChange={onChange}
              language={language?.value}
              theme={theme.value}
            />
        </section>
        <section className='bar'>
            <div>
             <ThemeDropdown handleThemeChange={handleThemeChange} theme={theme} />
            </div>
            <div>
              <LanguagesDropdown onSelectChange={onSelectChange} />
            </div>
        </section>
    </main>
  )
}

export default HomeScreen