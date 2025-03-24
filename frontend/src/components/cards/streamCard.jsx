import React from "react";
import {useNavigate} from "react-router-dom";

function StreamCard(
    {
        title,
        sportId,
        streamId,
        startTime,
        urls
    }
){
    const navigate = useNavigate()

    return(
        <section onClick={ () => navigate(`/stream/${streamId}`)}>
            <h2>{title}</h2>
            <p>{startTime}</p>
        </section>
    )
}

export default StreamCard;