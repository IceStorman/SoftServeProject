import React from "react";
import { NavLink } from "react-router-dom";
import useTranslations from "../../translationsContext";

function Logo() {
    const { t } = useTranslations();

    return (
        <NavLink to={"/"}className="nav-link" activeClassName="active">
        <div className="logo">
            <hr />
            <h1>{t("QSPORT")}</h1>
            <section className="subtitle">
                <hr/>
                    <p>{t("since")}</p>
                <hr/>
            </section>
            <hr />
        </div>
        </NavLink>
    )
}

export default Logo