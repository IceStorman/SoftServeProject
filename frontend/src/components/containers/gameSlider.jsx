import React, {useCallback, useState} from "react";
import GameCard from "../cards/gameCard";
import { useRef, useEffect } from "react";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import NoItems from "../NoItems";
import useTranslations from "../../translationsContext";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import {toast} from "sonner";


const GamesSlider = ({ sportId }) => {
    const sliderRef = useRef(null);
    const { t } = useTranslations();

    const observerRef = useRef(null);
    const [games, setGames] = useState([]);
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);
    const [gamesCount, setGamesCount] = useState(10);
    const [sportChanged, setSportChanged] = useState(false);

    const getGames = useCallback(async () => {

        if (!hasMore) return;

        const today = new Date().toISOString().split('T')[0];

        const filtersData = [
            { 'filter_name': 'date_from', 'filter_value': today },
            { 'filter_name': 'date_to', 'filter_value': today },
            { 'filter_name': 'sport_id', 'filter_value': sportId === "all" ? null : sportId }
        ].filter(f => f.filter_value !== null);

        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.games.getGames}`,
                {
                    pagination: {
                        page: page,
                        per_page: gamesCount,
                    },
                    filters: filtersData
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            if (response.data.items.length === 0) {
                setHasMore(false);
            } else {
                setPage(prev => prev + 1);
                setGames(prev => [...prev, ...response.data.items]);
            }
        } catch (error) {
            toast.error(`Troubles With games Loading: ${error}`);
        }
    }, [sportId, page, hasMore, gamesCount]);

    useEffect(() => {
        setGames([]);
        setPage(1);
        setHasMore(true);
        setSportChanged(true);
    }, [sportId]);

    useEffect(() => {
        if (sportChanged) {
            getGames();
            setSportChanged(false);
        }
    }, [games, sportChanged, getGames]);

    useEffect(() => {
        if (!games.length || !sliderRef.current) return;

        if (observerRef.current) observerRef.current.disconnect();

        observerRef.current = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting) {
                    getGames();
                }
            },
            { threshold: 1.0 }
        );

        const lastGameElement = sliderRef.current.lastChild;
        if (lastGameElement) observerRef.current.observe(lastGameElement);

        return () => {
            if (observerRef.current) observerRef.current.disconnect();
        };
    }, [games, getGames]);

    const scroll = (direction) => {
        if (sliderRef.current) {
            sliderRef.current.scrollBy({
                left: direction === "left" ? -600 : 600,
                behavior: "smooth"
            });
        }
    };


    return (
        <div className="games-slider-container">
            <div className="slider-controls">
                <button onClick={() => scroll("left")}><SlArrowLeft /></button>
                <button onClick={() => scroll("right")}><SlArrowRight /></button>
            </div>
            <div className="games-slider-outer" ref={sliderRef} onScroll={(e) => {
                const { scrollLeft, scrollWidth, clientWidth } = e.target;
                if (scrollLeft + clientWidth >= scrollWidth - 10) {
                    getGames();
                }
            }}>
                <div className="games-row">
                    { games.length > 0 ? (
                        games.map((item, index) => (
                            <GameCard
                                key={index}
                                nameHome={item.home_team_name}
                                nameAway={item.away_team_name}
                                logoHome={item.home_team_logo}
                                logoAway={item.away_team_logo}
                                scoreHome={item.home_score}
                                scoreAway={item.away_score}
                                time={item.time}
                                isVertical={true}
                            />
                        ))
                    ) : (
                        <NoItems key={1} text={t("games_not_found")} />
                    )}
                </div>
            </div>
        </div>
    );
};

export default GamesSlider;