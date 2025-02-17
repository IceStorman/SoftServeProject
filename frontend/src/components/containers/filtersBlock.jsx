import React from "react"
import useTranslations from "../../translationsContext";

const Filters = ({ }) => {
    const { t } = useTranslations();

    return (
        <div className="filters">
            <h1>{t("filters")}</h1>
            <hr />
            <p>{t("first_option")}</p>
            <p>{t("second_option")}</p>
            <p>{t("third_option")}</p>
        </div>
    );
}

export default Filters;