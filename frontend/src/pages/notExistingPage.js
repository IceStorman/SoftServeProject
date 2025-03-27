import React from "react";
import {Link} from "react-router-dom";
import globalVariables from "../globalVariables";

function NotExistingPage(){

    return(
        <section className={"notExistingPage"}>
            <h1>Sorry...</h1>
            <h1>Such page doesn't exist!</h1>
            <Link to={globalVariables.routeLinks.defaultRoute}>Return to main page</Link>
        </section>
    );
}

export default NotExistingPage;