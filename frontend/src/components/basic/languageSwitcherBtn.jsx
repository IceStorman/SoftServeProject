import React, {useEffect, useState} from 'react';
import useTranslations from '../../translationsContext';

function LanguageSwitcher(){
    const { changeLanguage, language } = useTranslations();

    const isEnglish = language === 'en';

    const [checked, setChecked] = useState(!isEnglish);

    useEffect(() => {
        setChecked(!isEnglish);
    }, [language]);

    const toggleLanguage = () => {
        const newLang = isEnglish ? "uk" : "en";
        changeLanguage(newLang);
        setChecked(!checked);
    };

    return (
        <div className={"languageSwitcher"}>
            <label htmlFor="filter" className={"switch"} aria-label="Toggle Language">
                <input
                    type="checkbox"
                    id="filter"
                    checked={checked}
                    onChange={toggleLanguage}
                />
                <span>EN</span>
                <span>UA</span>
            </label>
        </div>
    );
}

export default LanguageSwitcher;
