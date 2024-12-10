import React from "react";

function Games({logoHome, logoAway, time, teamHome, teamAway, league}){

    return(
        <div className="gamesBox">

            <img src={logoHome} alt={teamHome}/>

            <div className="gamesInfo">

                <h4 className="preview">{time}</h4>

                <h1 className="score">VS</h1>

                <img src={league} alt={teamAway}/>

            </div>

            <img src={logoAway} alt={teamAway}/>

        </div>
    );
}

export default Games;