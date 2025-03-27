import React, {useContext, useEffect, useState} from "react";
import {NavLink, useLocation, useNavigate} from "react-router-dom";
import useTranslations from "../../translationsContext";
import globalVariables from "../../globalVariables";
import {FaBars, FaTimes} from "react-icons/fa";
import clsx from "clsx";
import LanguageBtn from "./languageSwitcherBtn";
import LoginBtn from "./loginBtn";
import {User} from "lucide-react";
import {AuthContext} from "../../pages/registration/AuthContext";

function NavBar() {
    const { t } = useTranslations();
    const location = useLocation();

    const initialIcon = <FaBars size={28} />
    const navBar = (
        <>
            <NavLink to={globalVariables.routeLinks.defaultRoute} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("news")}</NavLink>
            <NavLink to={globalVariables.routeLinks.sportPageRoute} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("leagues")}</NavLink>
            <NavLink to={globalVariables.routeLinks.streamRoute} className={({ isActive }) => clsx("nav-link", { active: isActive })}>{t("games")}</NavLink>
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
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    return (
        <div className="navbar-outer">

            <div className={"navbar-box"}>
                {
                    burgerMenu ?
                        <button className={"menu-btn"} onClick={handleOpenMenu}> {menuIcon} </button>
                        :
                        <nav className="navbar">
                            {navBar}
                        </nav>
                }

                <div className={"btn-controller-box"}>

                    <LanguageBtn/>{
                    !user ? <LoginBtn/> :
                        <button className="account-button filled" onClick={() => navigate(globalVariables.routeLinks.accountRoute)}>
                            <User size={26} className="icon"/>
                        </button>
                    }

                </div>

            </div>

            <hr/>

            {
                <div className={`burger-nav ${menuIsOpen ? "show" : ""}`}>
                    {navBar}
                </div>
            }

        </div>
    );
}

export default NavBar