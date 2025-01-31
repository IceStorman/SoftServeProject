import React from "react";
import {Link, useParams} from "react-router-dom";

function TeamsBtn({team_name, teamId, sportId, logo}){
    const {sportName} = useParams
    return (
        <div className={"iconsBlockElement"}>

            <img src={logo} alt={team_name}/>
            <p>{team_name}</p>

        </div>
    );
}

export default TeamsBtn;