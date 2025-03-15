import React, { useState } from "react";
import GameCard from "../cards/gameCard";
import { useRef, useEffect } from "react";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import NoItems from "../NoItems";
import useTranslations from "../../translationsContext";


const GamesSlider = ({ games }) => {
    const sliderRef = useRef(null);
    const [canScrollLeft, setCanScrollLeft] = useState(false);
    const [canScrollRight, setCanScrollRight] = useState(true);
    const { t } = useTranslations();

    const checkScroll = () => {
        if (sliderRef.current) {
            const { scrollLeft, scrollWidth, clientWidth } = sliderRef.current;
            setCanScrollLeft(scrollLeft > 0);
            setCanScrollRight(scrollLeft + clientWidth < scrollWidth);
        }
    };

    const scroll = (direction) => {
        if (sliderRef.current) {
            const scrollAmount = 600; 
            sliderRef.current.scrollBy({ left: direction === "left" ? -scrollAmount : scrollAmount, behavior: "smooth" });
        }
    };

    useEffect(() => {
        if (sliderRef.current) {
            checkScroll();
            sliderRef.current.addEventListener("scroll", checkScroll);
        }
        return () => {
            if (sliderRef.current) {
                sliderRef.current.removeEventListener("scroll", checkScroll);
            }
        };
    }, []);

    return (
        <div className="games-slider-container">
            <div className="slider-controls">
                <button  onClick={() => scroll("left")} disabled={!canScrollLeft}><SlArrowLeft /></button>
                <button  onClick={() => scroll("right")} disabled={!canScrollRight}><SlArrowRight /></button>
            </div>
            <div className="games-slider-outer" ref={sliderRef}>
                <div className="game-category">
                    <div className="games-row">
                        {!(games.length === 0) ?
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
                                    height={160}
                                    width={300}
                                />
                            ))
                            : (
                                <NoItems
                                    key={1}
                                    text={t("games_not_found")}
                                />
                            )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GamesSlider;
