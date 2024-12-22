import React, {useState, useEffect, createContext, useContext} from "react";
import { Link } from "react-router-dom";
import axios from 'axios';

import apiEndpoints from "../apiEndpoints";

import News from "../components/mainPage/news.js"
import SportBtn from "../components/mainPage/sportBtn"
import Slider from "../components/games/slider.js";
import {toast} from "sonner";
import footer from "../components/footer";

function MainPage() {
    const [loginStatus,setLoginStatus]=useState(false)

    const [news, setNews] = useState([]);
    const [sports, setSport] = useState([]);
    const [games, setGames] = useState([]);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.news.getRecent}`)
            .then(res => {
                const returnedNews = res.data;
                setNews(returnedNews);
            })
            .catch(error => {
                toast.error(`:( Troubles With News Loading: ${error}`);
            });
    }, []);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.sports.getAll}`)
            .then(res => {
                const returnedSports = res.data;
                setSport(returnedSports);
            })
            .catch(error => {
                toast.error(`:( Troubles With Sports Loading: ${error}`);
            });
    }, []);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.games.getGames}`)
            .then(res => {
                const returnedGames = res.data;
                setGames(returnedGames);
            })
            .catch(error => {
                toast.error(`:( Troubles With Games Loading: ${error}`);
            });
    }, []);

    return(

        <>

            <Slider games={games} />

            <section className="container">

                <section className={`news ${loginStatus ? "narrow" : "wide wrapedNews"}`}>

                    <h1 className="newsTitle">НОВИНИ</h1>

                    {
                        !(news.length === 0) ?
                            news.map((item, index) => (
                                <News
                                    key={index}
                                    id={item.blob_id}
                                    title={item.data?.title}
                                    date={item.data?.timestamp}
                                    img={item.data?.images[0]}
                                    sport={item.data?.S_P_O_R_T}
                                />
                            ))
                            :
                            <div className={"noItems"}>
                                <h1>no latest news were found :(</h1>
                            </div>
                    }

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
                            sport={item.sport}
                            sportId={item.id}
                            img={item.logo}
                            sports={sports}
                        />
                    ))}

                </section>

            </section>

        </>
    );
}

export default MainPage;