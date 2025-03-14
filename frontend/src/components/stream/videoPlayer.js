import React, { useState } from "react";


const VideoPlayer = ({game, youtubeLinks = [], otherLinks = [] }) => {
    const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

    const handleVideoSwitch = (index) => {
        setCurrentVideoIndex(index);
    };

    return (
        <div className="videoContainer">

            <div className="videoPlayer">

                <div className="youtubePlayer">
                    {youtubeLinks.length > 0 ? (
                        <>
                            <iframe
                                title="YouTube Player"
                                width="100%"
                                height="500px"
                                src={`https://www.youtube.com/embed/${youtubeLinks[currentVideoIndex]}`}

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

                {otherLinks.length > 0 ? (
                    <>
                        <div className="partnerLinks">
                            <h2>Other:</h2>
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
                    </>
                    ): null}
            </div>
        </div>
    );
};

export default VideoPlayer;
