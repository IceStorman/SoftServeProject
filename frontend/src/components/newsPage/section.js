import React from "react";

function Section({text, img}){
    return(
        <>
            <p>{text}</p>
            <img src={img} />
        </>
    );
}

export default Section;