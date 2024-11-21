import React, {useState, useEffect} from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import News from "../components/mainPage/News.js"

/*const news =[
    {
        img: "/img/team.jpg",
        title: "Why did the programmer quit his job? Because he didn't get arrays.",
        date: "02.04.2006"
    },
    {
        img: "/img/team.jpg",
        title: "Why do Java developers wear glasses? Because they can't C#.",
        date: "11.12.2005"
    },
    {
        img: "/img/team.jpg",
        title: "There are only 10 types of people in the world: those who understand binary and those who don't.",
        date: "14.02.2006"
    }


];*/


function MainPage({news}) {
    const [loginStatus,setLoginStatus]=useState(true)

    return(

        <>

            <section className="streams">

                <button></button>

                <div className="streamsBar">

                    <div className="activeStreams">

                        <h2 id="liveStreams">Активні</h2>

                        <div className="streamBox">

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                            <div className="streamInfo">

                                <h4 className="online">етер</h4>

                                <h1 className="score">0:0</h1>

                                <h4 className="matchLeague">ліга</h4>

                            </div>

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                        </div>

                    </div>

                    <div className="scheduledStream">

                        <div id="plannedStreams">
                            <h2>MNS</h2>
                            <h2>00</h2>
                        </div>

                        <div className="streamBox">

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                            <div className="streamInfo">

                                <h4 className="preview">скоро</h4>

                                <h1 className="score">VS</h1>

                                <h4 className="matchLeague">ліга</h4>

                            </div>

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                        </div>

                    </div>

                </div>


                <button id="rightBtn"></button>

            </section>

            <section className="container">

                <section className={`news ${loginStatus ? "narrow" : "wide"}`}>

                    <h1 className="newsTitle">НОВИНИ</h1>

                    {news.slice(0, 5).map((item, index) => (
                        <News
                            key={index}
                            title={item.data?.header?.title}
                            text={item.data?.body}
                            img={item.data?.img}
                        />
                    ))}

                </section>

                {loginStatus ? (
                    <section className={`news ${loginStatus ? "narrow" : "wide"}`}>

                        <h1 className="newsTitle">РЕКОМЕНДАЦІЇ</h1>

                        <div className="newsBox">

                            <img src="/img/team.jpg" alt="news picture"/>

                            <div className="newsInsight">
                                <h1>TITLE BLA BLA BLA BLA</h1>
                                <h4 className="date">02.04.2024</h4>
                            </div>

                            <hr/>

                        </div>

                    </section>
                ) : null}


                <section className="navSports">

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/hero-banner.png" alt="footbal player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/basket-player.png" alt="basket player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/min-nba.png" alt="nba player"/>
                        </Link>


                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/mma-logo.png" alt="mma player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/handball-logo.png" alt="handball player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/hockey-logo.png" alt="hockey player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/afl-logo.png" alt="afl player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/baseball-logo.png" alt="baseball player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/rugby-logo.png" alt="rugby player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/volleyball-logo.png" alt="balleyball player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/nfl-logo.png" alt="nfl player"/>
                        </Link>

                    </div>

                    <div className="sportBox">

                        <Link to={"/"}>
                            <img src="/img/f1-mini.png" alt="formula player"/>
                        </Link>

                    </div>


                </section>

            </section>

        </>
    );
}

export default MainPage;