import React, {useContext} from "react";
import Logo from "./logo";
import LoginBtn from "./loginBtn";
import {AuthContext} from "../../pages/registration/AuthContext";


function Header() {
    const { user } = useContext(AuthContext);

    return (
        <header>
            <Logo />
            {
                !user ? <LoginBtn /> : null
            }
        </header>
    );
}


export default Header;
