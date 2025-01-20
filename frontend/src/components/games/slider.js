import React, { useState, useEffect, useRef  } from "react";
import ActiveGames from "./activeGames";

const Slider = ({ games }) => {
  const [visibleGames, setVisibleGames] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0); 
  const [clickCount, setClickCount] = useState(0); 
  const [translateValue, setTranslateValue] = useState(0); 
  const itemsPerSlide = 8;

  const sliderRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [currentTranslate, setCurrentTranslate] = useState(0);
  const [prevTranslate, setPrevTranslate] = useState(0);

  const remToPx = 16;

  const handleDragStart = (e) => {
    setIsDragging(true);
    setStartX(e.type.includes("mouse") ? e.pageX : e.touches[0].clientX);
    setCurrentTranslate(translateValue);
    sliderRef.current.style.transition = "none";
  };

  const handleDrag = (e) => {
    if (!isDragging) return;
  
    const currentPosition = e.type.includes("mouse") ? e.pageX : e.touches[0].clientX;
    const visibleWidth = sliderRef.current.clientWidth; 
   // console.log(currentIndex);
   // console.log(startX);
    const translateDelta = currentPosition - startX;
    //console.log(currentTranslate + (translateDelta / visibleWidth) * 100)
    setTranslateValue(currentTranslate + (translateDelta / visibleWidth) * 100);
  };

  const handleDragEnd = () => {
    setIsDragging(false);

    const closestIndex = Math.round(-translateValue / (100 / itemsPerSlide));
    const newTranslate = -closestIndex * (100 / itemsPerSlide);

    const remTranslate = newTranslate / 100 * remToPx;

    console.log(remTranslate);

    setTranslateValue( remTranslate);
    setPrevTranslate( remTranslate);
    setCurrentIndex(closestIndex * itemsPerSlide);

    const nextIndex = currentIndex + itemsPerSlide;
  
        if (nextIndex < games.length) {
          setVisibleGames((prevVisibleGames) => [
            ...prevVisibleGames,
            ...games.slice(nextIndex, nextIndex + itemsPerSlide),
          ]);
          setCurrentIndex(nextIndex);
        }

    sliderRef.current.style.transition = "transform 0.3s ease";
    sliderRef.current.style.transform = `translateX(${newTranslate}rem)`;
  }; 

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
            style={{ transform: `translate(${translateValue}rem)` }}
            
            ref={sliderRef}
            onMouseDown={handleDragStart}
            onMouseMove={handleDrag}
            onMouseUp={handleDragEnd}
            onMouseLeave={handleDragEnd}
            onTouchStart={handleDragStart}
            onTouchMove={handleDrag}
            onTouchEnd={handleDragEnd} 
            >
            
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
        
        <button id="rightBtn" onClick={onNext} disabled={currentIndex + itemsPerSlide >= games.length}></button>
        
        </section>
    )

}
export default Slider;