import React from "react";
import { NavLink } from "react-router-dom";

function Logo() {
    return (
        <NavLink to={"/"}className="nav-link" activeClassName="active">
        <div className="logo">
            <hr />
            <p> Certatum Nostrum </p>
            <section className="subtitle">
                <hr/>
                    <p>since 1990</p>
                <hr/>
            </section>
            <hr />
        </div>
        </NavLink>
    )
}

export default Logo