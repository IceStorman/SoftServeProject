import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

function useBurgerMenuState({
                                initialIcon,
                                closeIcon,
                                menuSelector = ".burger-nav",
                                buttonSelector = ".menu-btn"
                            }) {
    const [menuIsOpen, setMenuIsOpen] = useState(false);
    const [menuIcon, setMenuIcon] = useState(initialIcon);
    const location = useLocation(); // Отримуємо поточний шлях

    const handleCloseMenu = () => {
        setMenuIsOpen(false);
        setMenuIcon(initialIcon);
    };

    const handleOpenMenu = () => {
        setMenuIsOpen(prev => !prev);
        setMenuIcon(!menuIsOpen ? closeIcon : initialIcon);
    };

    // Закриває меню при зміні шляху
    useEffect(() => {
        handleCloseMenu();
    }, [location.pathname]);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (!event.target.closest(menuSelector) && !event.target.closest(buttonSelector)) {
                handleCloseMenu();
            }
        };

        const handleScrollOutside = () => {
            handleCloseMenu();
        };

        if (menuIsOpen) {
            document.addEventListener("mousedown", handleClickOutside);
            document.addEventListener("scroll", handleScrollOutside);
        }

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
            document.removeEventListener("scroll", handleScrollOutside);
        };
    }, [menuIsOpen, menuSelector, buttonSelector]);

    return { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu };
}

export default useBurgerMenuState;
