import { useState } from 'react';
import apiEndpoints from "./apiEndpoints";
import axios from 'axios';

const useLanguage = () => {
    const [language, setLanguage] = useState('en');

    const changeLanguage = async (newLang) => {
        try {
            await axios.get(`${apiEndpoints.url}${apiEndpoints.localization.setLanguage}/${newLang}`);
            setLanguage(newLang);
            document.cookie = `lang=${newLang}; path=/;`;
        } catch (error) {
            console.error("Error changing language:", error);
        }
    };

    return {
        language,
        changeLanguage
    };
};

export default useLanguage;
