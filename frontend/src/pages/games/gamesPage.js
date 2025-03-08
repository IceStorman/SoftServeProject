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
    const testGames1 =
        [
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
            }
        ]
    const [inputValue, setInputValue] = useState('');
    const [selectedTeam, setSelectedTeam] = useState("");
    const [selectedDate, setSelectedDate] = useState("");
    const [slidesCount, setSlidesCount] = useState(0);
    const gamesPerSlide = 10; // кількість ігор на слайд

    const handleChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleApplyFilters = () => {
        getGames(0); // Виконати запит з фільтрами
    };

    useEffect(() => {
        getGames(0);
    }, []);

    const applyFilters = () => {
        getGames();
    };
    const [currentGames, setCurrentGames] = useState([]);

    // const getGames = async (page) => {
    //     try {
    //         setLoading(true);
    //         const response = await axios.post(
    //             `${apiEndpoints.url}${apiEndpoints.games.getGames}`,
    //             {
    //                 page: page + 1,
    //                 per_page: gamesPerSlide
    //             },
    //             {
    //                 headers: { 'Content-Type': 'application/json' },
    //             }
    //         );
    //         console.log(response);
    //         setCurrentGames(response.data.games);
    //         const totalGames = response.data.count;
    //         setSlidesCount(Math.ceil(totalGames / gamesPerSlide));
    //     } catch (error) {
    //         setPageCount(0);
    //         toast.error(`Troubles With games Loading: ${error}`);
    //     }
    // };
    const getGames = async (page) => {
        try {
            // Формуємо параметри запиту з фільтрами
            const filters = {
                page: page + 1,
                per_page: gamesPerSlide,
                team: selectedTeam,  // Якщо вибрана команда
                date: selectedDate,   // Якщо вибрана дата
                search: inputValue,
            };

            // Очищаємо пусті значення
            Object.keys(filters).forEach(
                key => filters[key] === "" && delete filters[key]
            );

            // Виконуємо запит
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.games.getGames}`,
                filters,
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );
            console.log(response);
            setCurrentGames(response.data.games);
            const totalGames = response.data.count;
            setSlidesCount(Math.ceil(totalGames / gamesPerSlide));
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

                <GamesContainer >
                        {testGames1.map((item, index) => (
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
                </div>
        </div>
    );
}

export default GamesPage;