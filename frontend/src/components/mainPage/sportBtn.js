import React from "react";
import {Link} from "react-router-dom";

function SportBtn({sport, img}){

    return(
        <div className="sportBox">

            <Link to={"/"}>
                <img src={img} alt={sport}/>
            </Link>

        </div>
    );
}

export default SportBtn;