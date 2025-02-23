import {useEffect, useState} from 'react';
import apiEndpoints from "./apiEndpoints";
import axios from 'axios';
import {toast} from "sonner";
import Cookies from 'js-cookie';


const getCookie = (name) => {
    const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
    return match ? match[2] : null;
};

const useLanguage = () => {
    const [language, setLanguage] = useState(() => {
        return getCookie("lang") || localStorage.getItem("language") || "en";
    });

    useEffect(() => {
        Cookies.set('lang', language, { path: '/' });
        localStorage.setItem("language", language);
    }, [language]);

    const changeLanguage = async (newLang) => {
        try {
            await axios.get(`${apiEndpoints.url}${apiEndpoints.localization.setLanguage}/${newLang}`);
            setLanguage(newLang);
        } catch (error) {
            toast.error("Error changing language:", error);
        }
    };

    return {
        language,
        changeLanguage
    };
};

export default useLanguage;
