import React from "react";
import { Link } from "react-router-dom";
import globalVariables from "../../globalVariables";


function LeagueCard({ leagueName, img, id, sportId, size, sportName }) {
    const hideText = size === "medium" || size === "large";

    return (
        <Link to={`${globalVariables.routeLinks.sportPagePath}${sportName}${globalVariables.routeLinks.leaguePath}${leagueName}`} state={{leagueId: id, sportId: sportId, sportName: sportName}}>
            <div className={`league-card horizontal ${size}`}>
                {img && (
                    <div className={`image horizontal ${size}`}>
                        <img src={img} alt={leagueName} className="img-content"/>
                    </div>
                )}
                {!hideText && (
                    <div className={`content ${size}`}>
                        <h1>{leagueName}</h1>
                    </div>
                )}
            </div>
        </Link>
    );
}

export default LeagueCard;