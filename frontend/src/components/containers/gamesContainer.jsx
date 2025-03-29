import React from 'react';
import StreamCard from "../cards/streamCard";

const GamesContainer = ({
    streams
}) => {

    return (
        <div className="game-container">

            <div className='games'>

                {streams?.length > 0 ? streams.map((item) => (
                    <StreamCard
                        key={item?.id}
                        stream={item}
                    />
                )) : <p>No streams available</p>}

            </div>

        </div>
    );
};


export default GamesContainer;