import React, {useContext} from "react";
import Logo from "./logo";
import LoginBtn from "./loginBtn";
import LanguageBtn from "./languageSwitcherBtn";
import { User } from "lucide-react";
import {AuthContext} from "../../pages/registration/AuthContext";
import {useNavigate} from "react-router-dom";


function Header() {
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    return (
        <header>
            <Logo />
            <div className={"header-btn"}>
                {
                    !user ? <LoginBtn/> :
                        <button className="account-button filled" onClick={() => navigate("/user/account")}>
                            <User size={26} className="icon"/>
                        </button>
                }

            </div>

        </header>
    );
}


export default Header;
