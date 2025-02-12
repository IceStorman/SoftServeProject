import React, { useState } from "react";
import axios from "axios";
import ReactPaginate from 'react-paginate';
import { toast } from "sonner";

import NoItems from "../NoItems";
import GameCard from "../cards/gameCard";
import { useRef, useEffect } from "react";

import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
const GamesSlider = ({ testGames1 }) => {
    const sliderRef = useRef(null);
    const [canScrollLeft, setCanScrollLeft] = useState(false);
    const [canScrollRight, setCanScrollRight] = useState(true);

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
                {Object.entries(testGames1).map(([category, games]) => (
                    <div key={category} className="game-category">
                        <h2 className="category-title">{category}</h2>
                        <div className="games-row">
                            {games.map((item, index) => (
                                <GameCard
                                    key={index}
                                    nameHome={item.nameHome}
                                    nameAway={item.nameAway}
                                    logoHome={item.logoHome}
                                    logoAway={item.logoAway}
                                    scoreHome={item.scoreHome}
                                    scoreAway={item.scoreAway}
                                    time={item.time}
                                    height={160}
                                    width={300}
                                />
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default GamesSlider;
