import { createContext, useContext, useState } from "react"

export const ThemeContext = createContext(null)

export const ThemeContextProvider = ({ children }) => {
    const [mode, setMode] = useState("light")

    const toggleMode = () => {
        setMode((curr) => (curr == "light" ? "dark" : "light"))
    }
    return (
        <ThemeContext.Provider value={{ mode, toggleMode }}>
            {children}
        </ThemeContext.Provider>
    )
}

export const useModeToggle = () => {
    return useContext(ThemeContext)
}