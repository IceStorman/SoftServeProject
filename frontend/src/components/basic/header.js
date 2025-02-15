import React, {useContext} from "react";
import Logo from "./logo";
import LoginBtn from "./loginBtn";
import {AuthContext} from "../../pages/registration/AuthContext";


function Header() {
    const { user, logout } = useContext(AuthContext);

    return (
        <header>
            <Logo />
            {
                !user ? <LoginBtn /> : <button onClick={logout}>logout</button>
            }
        </header>
    );
}


export default Header;
