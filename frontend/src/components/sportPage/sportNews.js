import React from "react";

function SportNews({title, text, img, side, sport}){
    const placement = side === "right" ? ("leftPlaceData") : ""

    return (
        <>
            <div className="newsBox">

                {side === "left" ? (<img src={img} alt={sport}/>) : null}

                <div className="newsInsight">

                    <h1 className={placement}>{title}</h1>

                    <h4 className={`date ${placement}`}>{text}</h4>

                </div>

                {side === "right" ? (<img src={img} alt={sport}/>) : null}

            </div>
            <hr/>
        </>
    );
}

export default SportNews;