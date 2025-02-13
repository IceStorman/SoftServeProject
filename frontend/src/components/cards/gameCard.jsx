import React from "react";
import { NavLink } from "react-router-dom";

import img_placeholder from "../../pages/imgs/image_placeholder.png"


function GameCard({ nameHome, nameAway, logoHome, logoAway, scoreHome, scoreAway, time, id = 1, width, height }) {
    const isVertical = (width / height < 4);
    const isBig = true;

    return (
        <NavLink to={`/stream/${id}`} className="nav-link" activeClassName="active">
            <div
                className={`game-card ${isVertical ? "vertical" : "horizontal"}`}
                style={{ width: width, height: height }}
            >
                <h1 className="hometeam-name">{nameHome}</h1>

                {logoHome ? (
                    <img src={logoHome}
                        alt={' '}
                        className="hometeam-img"
                    />
                ) : (<img src={img_placeholder}
                    alt={nameHome}
                    className="hometeam-img"
                />)}

                <div className={`score-or-time ${isVertical ? "vertical" : "horizontal"}`}>
                    {scoreHome !== null && scoreAway !== null ? (
                        <p className="score">{scoreHome}:{scoreAway}</p>
                    ) : (
                        <div className="time">
                            <h3>VS</h3>
                            <p>{time}</p>
                        </div>
                    )}
                </div>
                <img src={logoAway}
                    alt={' '}
                    className="awayteam-img"
                />
                <h1 className="awayteam-name">{nameAway}</h1>
            </div>
        </NavLink>
    );
}

export default GameCard;