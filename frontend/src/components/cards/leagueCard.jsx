import React from "react";
import { Link } from "react-router-dom";

function LeagueCard({ leagueName, img, id, width, height, sportId }) {
    const isVertical = height >= width;

    return (
        <Link to={`league/${leagueName}`} state={{ leagueId: id, sportId:sportId}}>
        <div
            className={`league-card ${isVertical ? "vertical" : "horizontal"}`}
            style={{ width: width, height: height }}
        >
            {img && (
                <div className={isVertical ? "image vertical" : "image horizontal"}>
                    <img
                        src={img}
                        alt={leagueName}
                        className="img-content"
                    />
                </div>
            )}
            <div className={`content ${isVertical ? "vertical" : "horizontal"}`}>
                <div>
                    <h1>{leagueName}</h1>
                </div>
            </div>
        </div>
        </Link>
    );
}

export default LeagueCard;