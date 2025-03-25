import React, { useState } from 'react';
import { SlArrowDown, SlArrowUp } from "react-icons/sl";
import ReactPaginate from "react-paginate";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import StreamCard from "../cards/streamCard";

const GamesContainer = ({
    streams
}) => {

    return (
        <div className="game-container">

            <div className='games'>

                {streams?.length > 0 ? streams.map((item, index) => (
                    <StreamCard
                        title={item?.title}
                        sportId={item?.sport}
                        streamId={item?.id}
                        startTime={item?.start_time}
                        urls={item?.stream_url}
                    />
                )) : <p>No streams available</p>}

            </div>

        </div>
    );
};


export default GamesContainer;