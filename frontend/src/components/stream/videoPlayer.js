import React, { useState } from "react";

const VideoPlayer = ({game, youtubeLinks = [], otherLinks = [], matchInfo = {} }) => {
    const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

    const handleVideoSwitch = (index) => {
        setCurrentVideoIndex(index);
    };




    return (
        <div className="ramka">
            <div className="whoPlay">
                <h1>{game.name1} VS {game.name2}</h1>
                <div className="teams">
                    <div className="team">
                        <img src={game.logo1} alt={`${game.name1} logo`}/>
                    </div>
                    <div className="score">
                        {game.score1} : {game.score2}
                    </div>
                    <div className="team">
                        <img src={game.logo2} alt={`${game.name2} logo`}/>
                    </div>
                </div>
            </div>


            <div className="videoPlayer">

                <div className="youtubePlayer">
                    {youtubeLinks.length > 0 ? (
                        <>
                            <iframe
                                title="YouTube Player"
                                width="100%"
                                height="500px"
                                src={`https://www.youtube.com/embed/${youtubeLinks[currentVideoIndex]}`}
                                frameBorder="0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                            ></iframe>

                            {youtubeLinks.length > 1 && (
                                <div className="videoSwitcher">
                                    {youtubeLinks.map((link, index) => (
                                        <button
                                            key={index}
                                            className={`switchButton ${index === currentVideoIndex ? "active" : ""}`}
                                            onClick={() => handleVideoSwitch(index)}
                                        >
                                            Video {index + 1}
                                        </button>
                                    ))}
                                </div>
                            )}
                        </>
                    ) : (
                        <p>No YouTube streams available.</p>
                    )}
                </div>

                <div className="partnerLinks">
                    <h2>Or watch on our partners:</h2>
                    <div className="linksContainer">

                        {otherLinks.map((link, index) => (
                            <a href={link.url} target="_blank" rel="noopener noreferrer">
                                <div className="partnerLink">
                                    {link.name || `Partner ${index + 1}`}
                                </div>
                            </a>

                        ))}
                    </div>
                </div>
            </div>
            <div className="textInfo">
                {matchInfo && (
                    <section className="matchInfo">
                        <h3>{matchInfo.title}</h3>
                        <p>{matchInfo.description}</p>
                    </section>
                )}
            </div>
        </div>
    );
};

export default VideoPlayer;
