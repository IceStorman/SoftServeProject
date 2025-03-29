import React, { useContext, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import useTranslations from "../../translationsContext";
import globalVariables from "../../globalVariables";
import clsx from "clsx";
import LanguageBtn from "./languageSwitcherBtn";
import LoginBtn from "./loginBtn";
import { User } from "lucide-react";
import { AuthContext } from "../../pages/registration/AuthContext";
import useBurgerMenu from "../../customHooks/useBurgerMenu";
import useBurgerMenuState from "../../customHooks/useBurgerMenuState";
import { FaBars, FaTimes } from "react-icons/fa";

function NavBar() {
    const { t } = useTranslations();
    const navigate = useNavigate();
    const burgerMenu = useBurgerMenu(`${globalVariables.windowSizeForBurger.navBar}`);

    const { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu } = useBurgerMenuState({
        initialIcon: <FaBars size={28} />,
        closeIcon: <FaTimes size={28} color="black" />,
        menuSelector: ".burger-nav",
        buttonSelector: ".menu-btn"
    });

    const { user } = useContext(AuthContext);

    const navBar = (
        <>
            <NavLink to={globalVariables.routeLinks.defaultRoute} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("news")}</NavLink>
            <NavLink to={globalVariables.routeLinks.sportPageRoute} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("leagues")}</NavLink>
            <NavLink to={globalVariables.routeLinks.streamRoute} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("games")}</NavLink>
            <NavLink to={globalVariables.routeLinks.searchPageRoute} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("search")}</NavLink>
        </>
    );

    useEffect(() => {
        if (menuIsOpen) {
            const handleScroll = () => {
                handleCloseMenu();
            };

            window.addEventListener("scroll", handleScroll);

            return () => {
                window.removeEventListener("scroll", handleScroll);
            };
        }
    }, [menuIsOpen, handleCloseMenu]);

    return (
        <div className="navbar-outer">
            <div className="navbar-box">
                {burgerMenu ? (
                    <button className="menu-btn" onClick={handleOpenMenu}>
                        {menuIcon}
                    </button>
                ) : (
                    <nav className="navbar">{navBar}</nav>
                )}

                <div className="btn-controller-box">
                    <LanguageBtn />
                    {!user ? (
                        <LoginBtn />
                    ) : (
                        <button className="account-button filled" onClick={() => navigate(globalVariables.routeLinks.accountRoute)}>
                            <User size={26} className="icon" />
                        </button>
                    )}
                </div>

            </div>

            <hr />

            <div className={`burger-nav ${menuIsOpen ? "show" : ""}`}>{navBar}</div>
        </div>
    );
}

export default NavBar;