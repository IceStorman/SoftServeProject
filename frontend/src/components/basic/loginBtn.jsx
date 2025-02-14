import { NavLink } from "react-router-dom";
import React from "react";

function LoginBtn(){
    return (
        <button className="filled">
            <NavLink to={"/sign-in"} className="nav-link" activeClassName="active">Sign In</NavLink>
        </button>
    );
}

export default LoginBtn