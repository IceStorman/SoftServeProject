import React from "react";
import useTranslations from "../../translationsContext";


export const NameFilter = ({ onChange }) => {
    const {t} = useTranslations();

    return (
        <div className="filterSearch">
            <input type="text" placeholder={t("search_name")} onChange={onChange}/>
        </div>
    )
}