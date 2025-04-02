import { NavLink } from "react-router-dom";
import React from "react";
import useTranslations from "../../translationsContext";
import globalVariables from "../../globalVariables";

function LoginBtn(){
    const { t } = useTranslations();

    return (
        <button className="filled login">
            <NavLink to={globalVariables.routeLinks.signInRoute} className="nav-link" activeClassName="active">{t("log_in")}</NavLink>
        </button>
    );
}

export default LoginBtn