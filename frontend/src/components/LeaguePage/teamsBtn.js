import React from "react";
import {Link, useParams} from "react-router-dom";

function TeamsBtn({name, logo}){
    const {teamName} = useParams
    return (
        <Link className={"iconsBlockElement"} to={`/sport/${sportName}/teamName/${name}`} >

            <img src={logo} alt={name}/>

        </Link>
    );
}

export default TeamsBtn;