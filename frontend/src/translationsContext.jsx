import {createContext, useContext, useEffect, useState} from "react";
import axios from 'axios';
import apiEndpoints from "./apiEndpoints";
import {toast} from "sonner";
import useLanguage from './useLanguage';
import Cookies from 'js-cookie';


const TranslationsContext = createContext();

export const useTranslations = () => {
    return useContext(TranslationsContext);
};

export const TranslationsProvider = ({ children }) => {

    const { language, changeLanguage } = useLanguage();
    const [translations, setTranslations] = useState(() => {
        const cachedTranslations = Cookies.get(`translations_${language}`);
        return cachedTranslations ? JSON.parse(cachedTranslations) : null;
    });

    const loadTranslations = async (lang) => {
        try {
            const cached = Cookies.get(`translations_${lang}`);
            if (cached) {
                setTranslations(JSON.parse(cached));
                return;
            }

            const response = await axios.get(`${apiEndpoints.url}${apiEndpoints.localization.userBaseLanguage}`,{
                headers: {
                    "Accept-Language": lang,
                },
            });

            Cookies.set(`translations_${lang}`, JSON.stringify(response.data));
            setTranslations(response.data);
        } catch (error) {
            toast.error(`Error fetching translations: ${error}`);
            setTranslations({});
        }
    };

    useEffect(() => {
        if (language) {
            loadTranslations(language);
        }
    }, [language]);

    const t = (key) => translations && translations[key] ? translations[key] : key;
    return(
        <TranslationsContext.Provider value={{ t, changeLanguage, language }}>
            {children}
        </TranslationsContext.Provider>
    )
};


export default useTranslations;
