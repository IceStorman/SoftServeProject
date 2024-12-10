import React, { useState } from "react";
import Games from "./games";
import ActiveGames from "./activeGames";

const Slider = ({ games }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const itemsPerSlide = 4; 
  
    const getVisibleGames = () => {
      const start = currentIndex * itemsPerSlide;
      const end = start + itemsPerSlide;
      return games.slice(start, end);
    };
  
    const onNext = () => {
      setCurrentIndex((prevIndex) =>
        (prevIndex + 1) * itemsPerSlide >= games.length ? 0 : prevIndex + 1
      );
    };
  
    const onPrev = () => {
      setCurrentIndex((prevIndex) =>
        prevIndex === 0 ? Math.floor(games.length / itemsPerSlide) - 1 : prevIndex - 1
      );
    };

    return (
        <section className="games">
        
        <button onClick={onPrev}></button>
        
        <div className="gamesBar">
        
            <div className="activeGames">
                <h2 id="liveGames">Активні</h2>
        
                {getVisibleGames().slice(0, 4).map((item, index) => (
               <ActiveGames
                    key={index}
                    logoHome = {item?.teams?.home?.logo}
                    logoAway = {item?.teams?.away?.logo}
                    scoreHome = {item?.scores?.home}
                    scoreAway = {item?.scores?.away}
                    league = {item?.league?.logo}
                />
            ))}

            </div>
           
            <div className="scheduledGames">
           
                <div id="plannedGames">
                    <h2>MNS</h2>
                    <h2>00</h2>
                </div>
           
                {getVisibleGames().slice(0, 4).map((item, index) => (
               <Games
                    key={index}
                    logoHome = {item?.teams?.home?.logo}
                    logoAway = {item?.teams?.away?.logo}
                    league = {item?.league?.logo}
                    time = {item?.time}
                />
            ))}

            </div>
        
        </div>
        
        <button id="rightBtn" onClick={onNext}></button>
        
        </section>
    )

}
export default Slider;