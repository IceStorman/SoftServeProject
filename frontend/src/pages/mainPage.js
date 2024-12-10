import React, {useState, useEffect, createContext, useContext} from "react";
import { Link } from "react-router-dom";
import axios from 'axios';
import { Toaster, toast } from 'sonner'

import apiEndpoints from "../apiEndpoints";

import News from "../components/mainPage/news.js"
import SportBtn from "../components/mainPage/sportBtn"
import Slider from "../components/games/slider.js";

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
                let arr = [];
                returnedGames.forEach(element => {
                  element.matches.forEach(a => {
                    arr.push(a);
                  })
                });
                setGames(arr);
            })
            .catch(error => {
                toast.error(`:( Troubles With Games Loading: ${error}`);
            });
    }, []);

    return(

        <>

            <Toaster  position="top-center" expand={true} richColors  />

            <Slider games={games} />

            <section className="container">

                <section className={`news ${loginStatus ? "narrow" : "wide wrapedNews"}`}>

                    <h1 className="newsTitle">НОВИНИ</h1>

                    {news.map((item, index) => (
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