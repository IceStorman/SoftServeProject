import React from "react";
import { Link } from "react-router-dom";

function header(){

    return (

        <header>
            <Link className="title" to={"/"}>
                <span className="red">КУЙ</span>Sport
            </Link>

            <div className="nav-menu">

                <Link to={""}>Трансляції</Link>
                <Link to={""}>Розклад подій</Link>
                <Link className="sign-link" to={"/sign-in"}>Вхід</Link>

            </div>

        </header>

    );
}

export default header;