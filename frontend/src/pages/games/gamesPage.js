import React, { useState, useEffect, useRef } from "react";
import img1 from "../imgs/1.jpg"
import img2 from "../imgs/2.jpg"
import Filters from "../../components/containers/filtersBlock"
import GamesContainer from "../../components/containers/gamesContainer";
import GameCard from "../../components/cards/gameCard";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";

function GamesPage() {
    const [inputValue, setInputValue] = useState('');
    const [selectedTeam, setSelectedTeam] = useState("");
    const [selectedDate, setSelectedDate] = useState("");
    const [slidesCount, setSlidesCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [passedGames, setPassedGames] = useState(0);
    const gamesPerSlide = 20;

    useEffect(() => {
        let page = Math.floor(passedGames / gamesPerSlide);
        setCurrentPage(page);
        getGames(page);
    }, [gamesPerSlide]);

    useEffect(() => {
        getGames(0);
    }, []);

    const applyFilters = () => {
        getGames();
    };
    const [currentGames, setCurrentGames] = useState([]);

    const getGames = async (page) => {
        try {
            const filters = {
                team: selectedTeam,
                date: selectedDate,
                search: inputValue,
            };

            Object.keys(filters).forEach(
                key => filters[key] === "" && delete filters[key]
            );

            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.games.getGames}`,
                {
                    pagination: {
                        page: page + 1,
                        per_page: gamesPerSlide,
                    }
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );
            setCurrentGames(response.data.items);
            const totalGames = response.data.count;
            setSlidesCount(totalGames / gamesPerSlide);
        } catch (error) {
            setSlidesCount(0);
            toast.error(`Troubles with games loading: ${error}`);
        }
    };

    return (
        <div className="games-page">
            <Filters className='filters'
                     setSelectedTeam={setSelectedTeam}
                     setSelectedDate={setSelectedDate}
                     applyFilters={applyFilters}
                     setInputValue={setInputValue}
            />

            <div className="content">
                <GamesContainer postsPerPage={slidesCount}
                                currentPage={currentPage}
                                onPageChange={setCurrentPage}
                                pageCount={slidesCount}
                                paginationKey={currentPage}
                >
                    {currentGames.map((item, index) => (
                        <div className="game">
                            <GameCard
                                key={index}
                                nameHome={item.nameHome}
                                nameAway={item.nameAway}
                                logoHome={item.logoHome}
                                logoAway={item.logoAway}
                                scoreHome={item.home_score}
                                scoreAway={item.away_score}
                                time={item.time}
                                height={100}
                                width={700}
                            /></div>
                    ))},
                </GamesContainer>
            </div>
        </div>
    );
}

export default GamesPage;