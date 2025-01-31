import React from "react";
import {Link, useParams} from "react-router-dom";

function SportNews({title, text, img, side, sport, id}){
    const placement = side === "right" ? ("leftPlaceData") : "";
    const {sportName} = useParams();

    return (
        <>
            <Link className="newsBox" to={`/sport/${sportName}/news/${id}`} state={ id }>

                {side === "left" ? (<img src={img} alt={sport}/>) : null}

                <div className="newsInsight">

                    <h1 className={placement}>{title}</h1>

                    <h4 className={`date ${placement}`}>{text}</h4>

                </div>

                {side === "right" ? (<img src={img} alt={sport}/>) : null}

            </Link>

            <hr/>
        </>
    );
}

export default SportNews;