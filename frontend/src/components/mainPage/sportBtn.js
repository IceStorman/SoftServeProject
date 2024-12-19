import React from "react";
import {Link} from "react-router-dom";

function SportBtn({sport, img}){

    return (
            <Link className="sportBox" to={`/sport/${sport}`}>
                <img src={img} alt={sport}/>
            </Link>

    );
}

export default SportBtn;