import React from "react";

function News({title, text, img}){

    return (
        <div className="newsBox">

            <img src={img} alt="news picture"/>

            <div className="newsInsight">

                <h1>{title}</h1>

                <h4 className="date">{text}</h4>

            </div>

            <hr/>

        </div>
    );
}

export default News;