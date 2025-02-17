import React from 'react';
import useTranslations from '../../translationsContext';

const LanguageSwitcher = () => {
    const { t, changeLanguage } = useTranslations();

    const handleLanguageChange = (newLang) => {
        changeLanguage(newLang);
    };

    return (
        <div className="language-switcher-container">
            <button
                className="filled translate-first"
                onClick={() => handleLanguageChange('en')}
            >
                {t("english")}
            </button>
            <button
                className="filled translate-second"
                onClick={() => handleLanguageChange('uk')}
            >
                {t("ukrainian")}
            </button>
        </div>
    );
};

export default LanguageSwitcher;
