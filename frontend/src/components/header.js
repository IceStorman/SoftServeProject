import React from "react";
import { Link } from "react-router-dom";

function Header(){

    return (

        <header>
            <Link className="title" to={"/"}>
                <span className="red">КУЙ</span>Sport
            </Link>

            <div className="navMenu">

                <Link to={""}>Трансляції</Link>
                <Link to={""}>Розклад подій</Link>
                <Link className="signLink" to={"/sign-in"}>Вхід</Link>

            </div>

        </header>

    );
}

export default Header;