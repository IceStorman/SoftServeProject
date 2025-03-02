import React, {useContext} from "react";
import Logo from "./logo";
import LoginBtn from "./loginBtn";
import LanguageBtn from "./languageSwitcherBtn";
import {AuthContext} from "../../pages/registration/AuthContext";


function Header() {
    const { user, logout } = useContext(AuthContext);

    return (
        <header>
            <Logo />
            <div className={"header-btn"}>
                <LanguageBtn />
                {
                    !user ? <LoginBtn /> : <button className={"filled white"} onClick={logout}>logout</button>
                }
            </div>
        </header>
    );
}


export default Header;
