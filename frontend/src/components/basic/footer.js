import React from "react";
import { NavLink } from "react-router-dom";
import useTranslations from "../../translationsContext"
import { FaInstagram, FaGithub, FaFacebook } from "react-icons/fa";


function Footer() {

    const { t } = useTranslations();

    return (
        <footer>
            <div className="info-column">
                <h2>{t("navigation")}</h2>
                <NavLink to={"/"} className="nav-link" activeClassName="active">
                    <p>{t("main_page")}</p>
                </NavLink>
                <NavLink to={"/AboutUs"} className="nav-link" activeClassName="active">
                    <p>{t("about_us")}</p>
                </NavLink>
                <NavLink to={"/FAQ"} className="nav-link" activeClassName="active">
                    <p>{t("faq")}</p>
                </NavLink>
            </div>

            <div className="info-column">
                <h2>{t("contact_info")}</h2>
                <p>{t("address")}</p>
                <p>{t("phone")}</p>
                <p>{t("email")}</p>
            </div>

            <div className="info-column">
                <h2>{t("our_social_media")}</h2>
                <a href="https://github.com/IceStorman/SoftServeProject"
                   target="_blank"
                   rel="noopener noreferrer"
                   className={"social"}>
                    GitHub
                    <FaGithub/>
                </a>

                <a href="https://www.instagram.com/vladyslav_martynyshyn/"
                   target="_blank"
                   rel="noopener noreferrer"
                   className={"social"}>
                    Instagram<FaInstagram/>
                </a>

                <a href="https://www.facebook.com/profile.php?id=100018119430903"
                   target="_blank"
                   rel="noopener noreferrer"
                   className={"social"}>
                    Facebook<FaFacebook/>
                </a>
            </div>

        </footer>
    );
}

export default Footer;