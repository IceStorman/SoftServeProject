import React from "react";
import {Link} from "react-router-dom";

function LeagueBtn({name, logo}){

    return (
        <Link className={"iconsBlockElement"} to={`/league/${name}`}>

            <img src={logo} alt={name}/>

        </Link>
    );
}

export default LeagueBtn;