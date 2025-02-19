import React from "react";
import { NavLink } from "react-router-dom";

function NavBar() {
    return (
        <div className="navbar-outer">
            <nav className="navbar">
            <NavLink to={"/"} className="nav-link" activeClassName="active">News</NavLink>
            <NavLink to={"/sport"} className="nav-link" activeClassName="active">Leagues</NavLink>
            <NavLink to={"/stream"} className="nav-link" activeClassName="active">Games</NavLink>
            </nav>
            <hr />
        </div>
    );
}

export default NavBar