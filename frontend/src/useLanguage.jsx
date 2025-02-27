import {useEffect, useState} from 'react';
import Cookies from 'js-cookie';


const getCookie = (name) => Cookies.get(name);

const useLanguage = () => {
    const [language, setLanguage] = useState(() => {
        return getCookie("lang") || "en";
    });

    useEffect(() => {
        Cookies.set('lang', language, { path: '/' });
    }, [language]);

    const changeLanguage = (newLang) => {
        setLanguage(newLang);
    };

    return {
        language,
        changeLanguage
    };
};

export default useLanguage;
