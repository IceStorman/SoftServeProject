import React from "react";

import { useState } from "react";

function TeamCard({ leagueName: teamName, img, id, width, height, sportId }) {
    const [isFlipped, setIsFlipped] = useState(false);
    const isVertical = height >= width;

    const handleFlip = () => {
        setIsFlipped(!isFlipped);
    };

    return (
        <div
            className={`team-card ${isVertical ? "vertical" : "horizontal"} ${isFlipped ? "flipped" : ""}`}
            style={{ width, height }}
            onClick={handleFlip}
        >
                <div className={`team-card-front ${isVertical ? "vertical" : "horizontal"}`}>
                    {img && (
                        <div className={isVertical ? "image vertical" : "image horizontal"}>
                            <img src={img} alt={teamName} className="img-content" />
                        </div>
                    )}
                    <div className={`content ${isVertical ? "vertical" : "horizontal"}`}>
                        <h1>{teamName}</h1>
                    </div>
                </div>

                <div className="team-card-back">
                    <h2>hello</h2>
                    <p>how are u?</p>
                </div>
           
        </div>
    );
}


export default TeamCard;