import React from "react";
import {Link} from "react-router-dom";

function SportBtn({sport, sportId, img, sports}){

    return (
        <Link className="sportBox" to={`/sport/${sport}`} state={{sports, sportId}}>
            <img src={img} alt={sport}/>
        </Link>

    );
}

export default SportBtn;