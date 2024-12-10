import React from "react";

function ActiveGames({logoHome, logoAway, scoreHome, scoreAway, teamHome, teamAway, league}){

    return(
        <div className="gamesBox">

            <img src={logoHome} alt={teamHome}/>

            <div className="gamesInfo">

                <h4 className="online">етер</h4>

                <h1 className="score">{scoreHome}:{scoreAway}</h1>

                {/*<h4 className="matchLeague">{league}</h4>*/}

                <img src={league} alt={teamAway}/>

            </div>

            <img src={logoAway} alt={teamAway}/>

        </div>
    );
}

export default ActiveGames;