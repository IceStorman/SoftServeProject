import { useState, useEffect } from "react";
import globalVariables from "../globalVariables";


const useBurgerMenu = (width) => {
    const [burgerMenu, setBurgerMenu] = useState(false);

    useEffect(() => {

        const handleResize = () => {
            const smallScreen = window.innerWidth <= globalVariables.windowSizeForBurger.filters
            setBurgerMenu(smallScreen)
        }

        handleResize();
        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, []);

    return burgerMenu;
};

export default useBurgerMenu;
