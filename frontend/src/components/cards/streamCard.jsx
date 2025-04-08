import React from "react";
import {useNavigate} from "react-router-dom";
import globalVariables from "../../globalVariables";

function StreamCard(
    {
        stream
    }
){
    const navigate = useNavigate()

    return(
        <section className={"game"} onClick={() => navigate(`${globalVariables.routeLinks.streamPagePath}${stream?.id}`, { state: stream })}>
            <h2>{stream?.title}</h2>
            <p>{stream?.start_time}</p>
        </section>
    )
}

export default StreamCard;