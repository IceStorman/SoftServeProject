import React from "react";
import { NavLink } from "react-router-dom";

function Header(){

    return (

        <header>
            <NavLink className="title" to={"/"}>
                <span className="red">КУЙ</span>Sport
            </NavLink>

            <div className="navMenu">

                <NavLink to={"/stream"} className={({ isActive }) => (isActive ? 'activePage' : '')}>Трансляції</NavLink>
                <NavLink to={"/hui"} className={({ isActive }) => (isActive ? 'activePage' : '')}>Розклад подій</NavLink>
                <NavLink className="signLink" to={"/sign-in"}>Вхід</NavLink>

            </div>

        </header>

    );
}

export default Header;