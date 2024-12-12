import React from "react";
import {Link} from "react-router-dom";

function Team({name, logo}){

    return (
        <div className={"team"}>

            <Link to={`/league/${name}`}>

                <img src={logo} alt={name}/>

            </Link>

        </div>
    );
}

export default Team;