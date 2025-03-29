import { useState, useEffect } from "react";


const useBurgerMenu = (width) => {
    const [burgerMenu, setBurgerMenu] = useState(false);

    useEffect(() => {

        const handleResize = () => {
            const smallScreen = window.innerWidth <= width
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
