import React, {useEffect, useState} from "react";
import {NavLink, useLocation} from "react-router-dom";
import useTranslations from "../../translationsContext";
import globalVariables from "../../globalVariables";
import {FaBars, FaTimes} from "react-icons/fa";
import clsx from "clsx";

function NavBar() {
    const { t } = useTranslations();
    const location = useLocation();

    const initialIcon = <FaBars size={28} />
    const navBar = (
        <>
            <NavLink to={"/"} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("news")}</NavLink>
            <NavLink to={"/sport"} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("leagues")}</NavLink>
            <NavLink to={"/stream"} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("games")}</NavLink>
        </>
    )

    const [burgerMenu, setBurgerMenu] = useState(false)
    const [menuIsOpen, setMenuIsOpen] = useState(false)
    const [menuIcon, setMenuIcon] = useState(initialIcon)

    const handleCloseMenu = () => {
        setMenuIsOpen(false);
        setMenuIcon(initialIcon);
    }

    const handleOpenMenu = () => {
        setMenuIsOpen(prev => !prev)
        setMenuIcon(!menuIsOpen ? <FaTimes size={28} color="black" /> : initialIcon)
    }

    useEffect(() => {
        handleCloseMenu()
    }, [location.pathname]);

    useEffect(() => {

        const handleResize = () => {
            const smallScreen = globalVariables.windowsSizes.find(ws => window.innerWidth <= ws.maxWidth).maxWidth <= globalVariables.windowsSizes[0].maxWidth
            setBurgerMenu(smallScreen)
        }

        handleResize();
        window.addEventListener("resize", handleResize);
    }, []);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (!event.target.closest(".burger-nav")) {
                handleCloseMenu()
            }
        };

        const handleScrollOutside = () => {
            handleCloseMenu()
        }

        if (menuIsOpen) {
            document.addEventListener("mousedown", handleClickOutside);
            document.addEventListener("scroll", handleScrollOutside);
        }

    }, [menuIsOpen]);

    return (
        <div className="navbar-outer">

            {
                burgerMenu ?
                    <button className={"menu-btn"} onClick={handleOpenMenu}> {menuIcon} </button>
                    :
                    <nav className="navbar">
                        {navBar}
                    </nav>
            }

            <hr/>
            {
                menuIsOpen &&
                <div className={"burger-nav"}>
                    {navBar}
                </div>
            }

        </div>
    );
}

export default NavBar