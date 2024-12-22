import React from "react";

function Stream({logoHome, logoAway, scoreHome, scoreAway, teamHome, teamAway, league}){

    return(
        <div className="streamBox">

            <img src={logoHome} alt={teamHome}/>

            <div className="streamInfo">

                <h4 className="online">етер</h4>

                <h1 className="score">{scoreHome}:{scoreAway}</h1>

                <h4 className="matchLeague">{league}</h4>

            </div>

            <img src={logoAway} alt={teamAway}/>

        </div>
    );
}

export default Stream;