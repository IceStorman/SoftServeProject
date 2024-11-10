import React from "react";
import { Link } from "react-router-dom";

function MainPage() {


    return(
        <>

            <section className="streams">

                <button></button>

                <div className="streams-bar">

                    <div className="active-streams">

                        <h2 id="live-streams">Активні</h2>

                        <div className="stream-box">

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                            <div className="stream-info">

                                <h4 className="online">етер</h4>

                                <h1 className="score">0:0</h1>

                                <h4 className="match-league">ліга</h4>

                            </div>

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                        </div>

                    </div>

                    <div className="scheduled-stream">

                        <div id="planned-streams">
                            <h2>MNS</h2>
                            <h2>00</h2>
                        </div>

                        <div className="stream-box">

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                            <div className="stream-info">

                                <h4 className="preview">скоро</h4>

                                <h1 className="score">VS</h1>

                                <h4 className="match-league">ліга</h4>

                            </div>

                            <i className="fa fa-user-o" aria-hidden="true"></i>

                        </div>

                    </div>

                </div>


                <button id="right-btn"></button>

            </section>

            <section className="container">

                <section className="news">

                    <h1 className="news-title">НОВИНИ</h1>

                    <div className="news-box">

                        <img src="/img/team.jpg" alt="news picture"/>

                        <div className="news-insight">

                            <h1>TITLE BLA BLA BLA BLA</h1>

                            <h4 className="date">02.04.2024</h4>

                        </div>

                        <hr/>

                    </div>

                </section>

                <section className="news">

                    <h1 className="news-title">РЕКОМЕНДАЦІЇ</h1>

                    <div className="news-box">

                        <img src="/img/team.jpg" alt="news picture"/>

                        <div className="news-insight">

                            <h1>TITLE BLA BLA BLA BLA</h1>

                            <h4 className="date">02.04.2024</h4>

                        </div>

                        <hr/>

                    </div>

                </section>

                <section className="nav-sports">

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/hero-banner.png" alt="footbal player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/basket-player.png" alt="basket player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/min-nba.png" alt="nba player"/>
                        </Link>


                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/mma-logo.png" alt="mma player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/handball-logo.png" alt="handball player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/hockey-logo.png" alt="hockey player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/afl-logo.png" alt="afl player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/baseball-logo.png" alt="baseball player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/rugby-logo.png" alt="rugby player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/volleyball-logo.png" alt="balleyball player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

                        <Link to={"/"}>
                            <img src="/img/nfl-logo.png" alt="nfl player"/>
                        </Link>

                    </div>

                    <div className="sport-box">

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