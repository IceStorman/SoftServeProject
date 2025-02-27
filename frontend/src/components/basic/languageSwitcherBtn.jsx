import React from 'react';
import useTranslations from '../../translationsContext';

const LanguageSwitcher = () => {
    const { t, changeLanguage, language } = useTranslations();

    const languages = [
        { code: 'en', label: 'EN' },
        { code: 'uk', label: 'UA' },
    ];

    const handleLanguageChange = (newLang) => {
        changeLanguage(newLang);
    };

    return (
        <div className="language-switcher-container">
            {languages.map((lang) => (
                <button
                    key={lang.code}
                    className={`language-button ${language === lang.code ? 'active' : ''}`}
                    onClick={() => handleLanguageChange(lang.code)}
                >
                    {lang.label}
                </button>
            ))}
        </div>
    );
};

export default LanguageSwitcher;
