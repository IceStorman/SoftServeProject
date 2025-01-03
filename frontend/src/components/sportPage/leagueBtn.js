import React from "react";
import {Link, useParams} from "react-router-dom";

function LeagueBtn({name, logo}){
    const {sportName} = useParams();

    return (
        <Link className={"iconsBlockElement"} to={`/sport/${sportName}/league/${name}`}>

            <img src={logo} alt={name}/>

        </Link>
    );
}

export default LeagueBtn;