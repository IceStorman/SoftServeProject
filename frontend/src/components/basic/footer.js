import React from "react";
import { NavLink } from "react-router-dom";

function Footer() {

    return (
        <footer>
            <div className="info-column">
                <h2>Navigation</h2>
                <NavLink to={"/"} className="nav-link" activeClassName="active">
                    <p>Main page</p>
                </NavLink>
                <NavLink to={"/AboutUs"} className="nav-link" activeClassName="active">
                    <p>About us</p>
                </NavLink>
                <NavLink to={"/FAQ"} className="nav-link" activeClassName="active">
                    <p>FAQ</p>
                </NavLink>
            </div>

            <div className="info-column">
                <h2>Contact info</h2>
                <p>Address</p>
                <p>Phone</p>
                <p>Email</p>
            </div>

            <div className="info-column">
                <h2>Follow Us on Social Media</h2>
            </div>

            <div className="info-column">
                <h2>Subscribe to our newsletter</h2>
            </div>
        </footer>
    );
}

export default Footer;