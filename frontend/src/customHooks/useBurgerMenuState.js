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
    const location = useLocation();

    const handleCloseMenu = () => {
        setMenuIsOpen(false);
        setMenuIcon(initialIcon);
    };

    const handleOpenMenu = () => {
        setMenuIsOpen((prev) => {
            const newState = !prev;
            setMenuIcon(newState ? closeIcon : initialIcon);
            return newState;
        });
    };

    useEffect(() => {
        handleCloseMenu();
    }, [location.pathname]);

    useEffect(() => {
        if (!menuIsOpen) return;

        const handleClickOutside = (event) => {
            if (
                !event.target.closest(menuSelector) &&
                !event.target.closest(buttonSelector)
            ) {
                handleCloseMenu();
            }
        };

        document.addEventListener("mousedown", handleClickOutside);

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [menuIsOpen]);

    return { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu };
}

export default useBurgerMenuState;
