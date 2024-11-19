import React from "react";

function News({title, date, img}){


    return (
        <div className="newsBox">

            <img src={img} alt="news picture"/>

            <div className="newsInsight">

                <h1>{title}</h1>

                <h4 className="date">{date}</h4>

            </div>

            <hr/>

        </div>
    );
}

export default News;