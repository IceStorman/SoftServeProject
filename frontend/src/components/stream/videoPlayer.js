import React, { useState } from "react";

const VideoPlayer = ({ youtubeLinks = [], otherLinks = [], matchInfo = {}, whoPlay }) => {
    const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

    const handleVideoSwitch = (index) => {
        setCurrentVideoIndex(index);
    };


    return (
        <div className="ramka">
            <div className="whoPlay">
                <h2>{whoPlay}</h2>
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
