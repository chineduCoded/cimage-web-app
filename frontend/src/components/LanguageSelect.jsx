import React, { useState } from 'react';
import { languageOptions } from '../constants/languageOptions';
import "./styles.css";

const LanguageSelect = ({ onSelectChange }) => {
  const [selectedLanguage, setSelectedLanguage] = useState(languageOptions[0].value);

  const handleLanguageChange = (e) => {
    const selectedValue = e.target.value;
    setSelectedLanguage(selectedValue);
    onSelectChange(selectedValue);
  };

  return (
    <div>
      <select
        name='languages'
        value={selectedLanguage}
        onChange={handleLanguageChange}
        className='selected-option'
      >
        {languageOptions.map((language) => (
          <option key={language.value} value={language.value}>
            {language.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelect;