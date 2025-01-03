import React, { useState, useEffect  } from "react";
import ActiveGames from "./activeGames";

const Slider = ({ games }) => {
  const [visibleGames, setVisibleGames] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0); 
  const [clickCount, setClickCount] = useState(0); 
  const [translateValue, setTranslateValue] = useState(0); 
  const itemsPerSlide = 8;

  useEffect(() => {
    setVisibleGames(games.slice(0, itemsPerSlide)); 
  }, [games]);
  
    const onNext = () => {

      if (clickCount % 2 === 0) {
        const nextIndex = currentIndex + itemsPerSlide;
  
        if (nextIndex < games.length) {
          setVisibleGames((prevVisibleGames) => [
            ...prevVisibleGames,
            ...games.slice(nextIndex, nextIndex + itemsPerSlide),
          ]);
          setCurrentIndex(nextIndex);
        }
      }
  
      setTranslateValue((prevTranslate) => prevTranslate - 50);
      setClickCount((prevCount) => prevCount + 1);
      
    };
  
    const onPrev = () => {
      if (translateValue === 0) return; 
      setTranslateValue((prevTranslate) => prevTranslate + 50);
      setCurrentIndex((prevIndex) => (prevIndex === 0 ? 0 : prevIndex - 1));
    };

    return (
        <section className="games">
        
        <button onClick={onPrev} disabled={translateValue === 0}></button>
        
        <div className='gamesBar'>
        
            <div className='activeGames'
            style={{ transform: `translate(${translateValue}rem)` }}>
            
                <h2 id="liveGames">Активні</h2>
        
                {visibleGames.map((item, index) => (
               <ActiveGames
                    key={index}
                    logoHome = {item?.home_team_logo}
                    logoAway = {item?.away_team_logo}
                    scoreHome = {item?.home_score}
                    scoreAway = {item?.away_score}
                    league = {item?.league_logo}
                />
            ))}

            </div>
        
        </div>
        
        <button id="rightBtn" onClick={onNext}></button>
        
        </section>
    )

}
export default Slider;