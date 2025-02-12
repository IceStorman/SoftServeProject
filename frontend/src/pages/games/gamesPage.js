import React, { useState, useEffect, useRef } from "react";
import axios from 'axios';
import apiEndpoints from "../../apiEndpoints";
import { toast } from "sonner";

import img1 from "../imgs/1.jpg"
import img2 from "../imgs/2.jpg"
import img3 from "../imgs/3.jpg"
import img4 from "../imgs/4.jpg"
import img5 from "../imgs/5.jpg"



import Filters from "../../components/containers/filtersBlock"
import GamesContainer from "../../components/containers/gamesContainer";
import GameCard from "../../components/cards/gameCard";

function GamesPage() {
    const testGames1 =
    {
        category1: [{
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },{
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            time: "01/12/25"
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },],

        category2: [{
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },{
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            time: "01/12/25"
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },]
    }
    const [inputValue, setInputValue] = useState('');

    const handleChange = (event) => {
        setInputValue(event.target.value);
    };

    return (
        <div className="games-page">
            <Filters className='filters'></Filters>



            <div className="content">
                <input
                    type="text"
                    value={inputValue}
                    onChange={handleChange}
                    placeholder="Search..."
                    className="input-field"
                ></input>
                {Object.entries(testGames1).map(([category, games]) => (
                    <GamesContainer key={category} title={category}>
                        {games.map((item, index) => (
                            <div className="game">
                                <GameCard

                                    key={index}
                                    nameHome={item.nameHome}
                                    nameAway={item.nameAway}
                                    logoHome={item.logoHome}
                                    logoAway={item.logoAway}
                                    scoreHome={item.scoreHome}
                                    scoreAway={item.scoreAway}
                                    time={item.time}
                                    height={100}
                                    width={700}

                                /></div>
                        ))}
                    </GamesContainer>
                ))}</div>
        </div>
    );
}

export default GamesPage;