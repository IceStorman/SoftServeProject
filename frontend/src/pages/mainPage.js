import React, {useState, useEffect, createContext, useContext} from "react";
import { Link } from "react-router-dom";
import axios from 'axios';
import apiEndpoints from "../apiEndpoints";

import News from "../components/mainPage/news.js"
import SportBtn from "../components/mainPage/sportBtn"

function MainPage() {
    const [loginStatus,setLoginStatus]=useState(false)

    const [news, setNews] = useState([]);
    const [sports, setSport] = useState([]);


    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.news.getRecent}`)
            .then(res => {
                const returnedNews = res.data;
                setNews(returnedNews);
            })
            .catch(error => {
                console.error('There was an error getting news:', error);
            });
    }, []);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.sports.getAll}`)
            .then(res => {
                const returnedSports = res.data;
                setSport(returnedSports);
            })
            .catch(error => {
                console.error('There was an error getting sports:', error);
            });
    }, []);

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
                            title={item.data?.title}
                            text={item.data?.timestamp}
                            img={item.data?.images[0]}
                            sport={item.data?.S_P_O_R_T}
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

                    {sports.map((item, index)=>(
                        <SportBtn
                            key={index}
                            sport={item.sport_name}
                            img={item.sport_img}
                        />
                    ))}

                </section>

            </section>

        </>
    );
}

export default MainPage;