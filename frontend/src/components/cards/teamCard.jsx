import React from "react";

import { useState } from "react";

function TeamCard({ leagueName: teamName, img, id, size, sportId}) {
    const [isFlipped, setIsFlipped] = useState(false);
    const hideText = size === "medium" || size === "large";

    const handleFlip = () => {
        setIsFlipped(!isFlipped);
    };

    return (
        <div
            className={`team-card  horizontal ${size} ${isFlipped ? "flipped" : ""}`}
            onClick={handleFlip}
        >
            <div className="team-card-front">
                {img && (
                    <div className={`image horizontal ${size}`}>
                        <img src={img} alt={teamName} className="img-content"/>
                    </div>
                )}
                {!hideText && (
                    <div className={`content ${size}`}>
                        <h1>{teamName}</h1>
                    </div>
                )}
            </div>

            <div className="team-card-back">
                <h2>hello</h2>
                <p>how are u?</p>
            </div>
        </div>
    );
}


export default TeamCard;