import React from 'react';
import useTranslations from '../../translationsContext';

const LanguageSwitcher = () => {
    const { t, changeLanguage, language } = useTranslations();

    const handleLanguageChange = (newLang) => {
        changeLanguage(newLang);
    };

    return (
        <div className="language-switcher-container">
            <button
                className={`language-button ${language === 'en' ? 'active' : ''}`}
                onClick={() => handleLanguageChange('en')}
            >
                EN
            </button>
            <span className="language-separator">/</span>
            <button
                className={`language-button ${language === 'uk' ? 'active' : ''}`}
                onClick={() => handleLanguageChange('uk')}
            >
                UA
            </button>
        </div>
    );
};

export default LanguageSwitcher;
