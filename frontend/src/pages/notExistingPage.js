import React from "react";
import {Link} from "react-router-dom";

function NotExistingPage(){

    return(
        <section className={"notExistingPage"}>
            <h1>Sorry...</h1>
            <h1>Such page doesn't exist!</h1>
            <Link to={"/"}>Return to main page</Link>
        </section>
    );
}

export default NotExistingPage;