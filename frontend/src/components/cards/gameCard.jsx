import React from "react";


function GameCard({ nameHome, nameAway, logoHome, logoAway, scoreHome, scoreAway, time, isVertical }) {
    const layoutClass = isVertical ? "vertical" : "horizontal";

    return (
        <div className={`game-card ${layoutClass}`}>
            <h1 className="hometeam-name">{nameHome}</h1>

            {logoHome ? (
                <img src={logoHome}
                    alt={' '}
                    className="hometeam-img"
                />
            ) : (<img src={""}
                alt={nameHome}
                className="hometeam-img"
            />)}

            <div className={`score-or-time ${layoutClass}`}>
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
    );
}

export default GameCard;