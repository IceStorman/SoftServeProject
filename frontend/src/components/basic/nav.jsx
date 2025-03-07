import React from "react";
import { NavLink } from "react-router-dom";
import useTranslations from "../../translationsContext";

function NavBar() {
    const { t } = useTranslations();

    return (
        <div className="navbar-outer">
            <nav className="navbar">
            <NavLink to={"/"} className="nav-link" activeClassName="active">{t("news")}</NavLink>
            <NavLink to={"/sport"} className="nav-link" activeClassName="active">{t("leagues")}</NavLink>
            <NavLink to={"/stream"} className="nav-link" activeClassName="active">{t("games")}</NavLink>
            </nav>
            <hr />
        </div>
    );
}

export default NavBar