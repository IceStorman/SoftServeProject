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

    const TRANSLATION_VERSION_KEY = "translation_version";
    const TRANSLATION_COOKIE_PREFIX = "translations_";

    const getTranslationVersion = async () => {
        try {
            const response = await axios.get(`${apiEndpoints.url}${apiEndpoints.localization.ver}`);
            return response.data.version;
        } catch (error) {
            toast.error("Error fetching translation version:", error);
            return null;
        }
    };

    const loadTranslations = async (lang) => {
        try {
            const latestVersion = await getTranslationVersion();
            if (!latestVersion) return;

            const cacheKey = `${TRANSLATION_COOKIE_PREFIX}${latestVersion}_${lang}`;
            const cachedVersion = Cookies.get(TRANSLATION_VERSION_KEY);
            const cachedTranslations = Cookies.get(cacheKey);

            if (cachedVersion === latestVersion && cachedTranslations) {
                setTranslations(JSON.parse(cachedTranslations));
                return;
            }

            const response = await axios.get(`${apiEndpoints.url}${apiEndpoints.localization.userBaseLanguage}`, {
                headers: { "Accept-Language": lang },
            });

            Object.keys(Cookies.get()).forEach((cookieKey) => {
                if (cookieKey.startsWith(TRANSLATION_COOKIE_PREFIX)) {
                    Cookies.remove(cookieKey);
                }
            });

            Cookies.set(cacheKey, JSON.stringify(response.data), { expires: 7 });
            Cookies.set(TRANSLATION_VERSION_KEY, latestVersion, { expires: 7 });

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
