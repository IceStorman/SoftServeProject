import React from "react";
import {Link} from "react-router-dom";


function News({title, date, img, sport, id}){

    return (

        <Link className="newsBox" to={`/news/${id}`} state={ id }>

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