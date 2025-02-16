import React from "react";
import Logo from "./logo";
import LoginBtn from "./loginBtn";
import LanguageBtn from "./languageSwitcherBtn";

function Header() {
    return (
        <header>
            <Logo />
            <LoginBtn />
            <LanguageBtn />
        </header>
    );
}


export default Header;
