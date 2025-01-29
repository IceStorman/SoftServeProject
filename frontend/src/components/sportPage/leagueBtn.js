import React from "react";
import {Link, useParams} from "react-router-dom";

function LeagueBtn({leagueName, logo, leagueId, sportId}){
    const {sportName} = useParams();

    return (
        <Link className={"iconsBlockElement"} to={`/sport/${sportName}/league/${leagueName}`} state={{leagueId, sportId}}>

                <img src={logo} alt={leagueName}/>

        </Link>
    );
}

export default LeagueBtn;