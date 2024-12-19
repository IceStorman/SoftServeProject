import React from "react";
import {Link} from "react-router-dom";


function News({title, date, img, sport, id}){
    const words = title.split(/[\s.,\/#!$%\^&\*;:{}=\-_`~()@\[\]'"<>?|\\+]+/).join('-');
    const link = id + "-" + words;

    return (

        <Link className="newsBox" to={`/news/${link}`}>

            <img src={img} alt={sport}/>

            <div className="newsInsight">

                <h1>{title}</h1>

                <h4 className="date">{date}</h4>

            </div>

            <hr/>

        </Link>
    );
}

export default News;