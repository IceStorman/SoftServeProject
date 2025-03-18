import React from 'react';
import useTranslations from '../../translationsContext';

function LanguageSwitcher(){
    const { changeLanguage, language } = useTranslations();

    const isEnglish = language === 'en';

    const toggleLanguage = () => {
        changeLanguage(isEnglish ? 'uk' : 'en');
    };

    return (
        <div className={"languageSwitcher"}>
            <div className="flipswitch">
                <input
                    id="lang-switch"
                    className="flipswitch-cb"
                    type="checkbox"
                    checked={isEnglish}
                    onChange={toggleLanguage}
                />
                <label htmlFor="lang-switch" className="flipswitch-label">
                    <div className="flipswitch-inner">
                        <span className="flipswitch-en">EN</span>
                        <span className="flipswitch-ua">UA</span>
                    </div>
                    <div className="flipswitch-switch"/>
                </label>
            </div>
        </div>
    );
};

export default LanguageSwitcher;
