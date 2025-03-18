import { NavLink } from "react-router-dom";
import React from "react";
import useTranslations from "../../translationsContext";

function LoginBtn(){
    const { t } = useTranslations();

    return (
        <button className="filled login">
            <NavLink to={"/sign-in"} className="nav-link" activeClassName="active">{t("log_in")}</NavLink>
        </button>
    );
}

export default LoginBtn