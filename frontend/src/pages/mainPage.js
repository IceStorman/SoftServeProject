import React, {useState, useEffect} from "react";
import axios from 'axios';

import apiEndpoints from "../apiEndpoints";

import News from "../components/mainPage/news.js"
import SportBtn from "../components/mainPage/sportBtn"
import Slider from "../components/games/slider.js";
import {toast} from "sonner";
import NoItems from "../components/NoItems";

function MainPage() {
    const [loginStatus,setLoginStatus]=useState(false)

    const [news, setNews] = useState([]);
    const [sports, setSport] = useState([]);
    const [games, setGames] = useState([]);

    const [loading, setLoading] = useState(false)

    useEffect(() => {

        setLoading(true)

        axios.get(`${apiEndpoints.url}${apiEndpoints.news.getRecent}`)
            .then(res => {
                const returnedNews = res.data;
                setNews(returnedNews);
            })
            .catch(error => {
                toast.error(`:( Troubles With News Loading: ${error}`);
            })

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

    useEffect(() => {
        (news.length > 0 || sports.length > 0 || games.length) ? setLoading(false)
        : setTimeout(() => {
            setLoading(false);
        }, 2000)
    }, [news.length, sports.length, games.length]);

    return(

        <>

            <Slider games={games}/>

            <section className="container">

                <section className={`news ${loginStatus ? "narrow" : "wide wrappedNews"}`}>

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
                            : (loading === false) ?
                                (
                                    <NoItems
                                        key={1}
                                        text={"No latest news were found"}
                                    />
                                ) : null
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

                    {sports.map((item, index) => (
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

            {loading === true ?
                (
                    <>
                        <div className={"loader-background"}></div>
                        <div className="loader"></div>
                    </>
                ) : null
            }

        </>
    );
}

export default MainPage;