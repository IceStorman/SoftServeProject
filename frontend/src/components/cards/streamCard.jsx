import React from "react";
import {useNavigate} from "react-router-dom";

function StreamCard(
    {
        stream
    }
){
    const navigate = useNavigate()

    return(
        <section className={"game"} onClick={() => navigate(`/stream/${stream?.id}`, { state: stream })}>
            <h2>{stream?.title}</h2>
            <p>{stream?.start_time.split('T')[0]}</p>
        </section>
    )
}

export default StreamCard;