import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import NewsSection from "../components/newsPage/newsSection";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";
import NoItems from "../components/NoItems";

function NewsPage(){
    const {sportName,id} = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const newsId = location.state || id;
    const [likes, setLikes] = useState(0);
    const [liked, setLiked] = useState(false);

    const [news, setNews] = useState([]);

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        const fetchNews = async () => {
            try {
                setLoading(true);

                const response = await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.news.getArticle}`,
                    {
                        blob_id: newsId,
                    },
                    {
                        headers: { 'Content-Type': 'application/json' },
                    }
                );

                if(sportName !== undefined){
                    if(response.data[0].data.S_P_O_R_T !== sportName) {
                        navigate("/not-existing")
                    }
                }

                if(response.data.likes === undefined){
                    setLikes(0);
                }

                setNews(response.data[0].data);
                setLikes(response.data.likes);
            } catch (error) {
                if(news.length === 0) {
                    navigate("/not-existing")
                }
                toast.error(`:( Troubles With This News Loading: ${error}`);
            }
        };

        fetchNews();
    }, []);


    const handleLike = async () => {
        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.news.likeArticle}`,
                {
                    like: newsId,
                },
                {headers: {"Content-Type": "application/json"}}
            );

            if (response.status === 200) {
                setLikes((prevLikes) => prevLikes + 1);
                setLiked(true);
            }
        } catch (error) {
            toast.error(`:( Troubles With Your Like: ${error}`);
        }
    };


    useEffect(() => {
        (news?.title) ? setLoading(false)
            : setTimeout(() => {
                setLoading(false);
            }, 2000)
    }, [news]);


    useEffect(() => {
        if(likes === undefined){
            setLikes(0);
        }
    }, [likes]);

    
    return(
        <>
            <section className={"newsContent"}>
                {!(news.length === 0) ? (

                    <>
                        <h1>{news?.title}</h1>

                        {news?.article &&
                            Object.entries(news.article).map(([key, value], index) => (
                                <NewsSection
                                    key={key}
                                    text={value?.content}
                                    teams={news?.team_names[0]}
                                    subheading={value?.subheadings}
                                    img={news?.images?.[index]}
                                    newsId={newsId}
                                />
                            ))
                        }

                        <div className="likeButtonContainer">
                            <button
                                className={`likeButton ${liked ? "liked" : ""}`}
                                onClick={handleLike}
                                disabled={liked}
                            >
                                {liked ? `${likes} Likes ❤️` : `${likes} Likes 🤍`}
                            </button>

                            <h4 className="date">{news?.timestamp}</h4>

                        </div>
                    </>
                ) : (loading === false) ?
                    (
                        <NoItems
                            key={1}
                            text={"no such news was found"}
                        />
                    ) : null
                }

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

export default NewsPage;