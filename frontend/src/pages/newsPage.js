import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import NewsSection from "../components/newsPage/newsSection";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";

function NewsPage(){
    const {sportName,id} = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const newsId = location.state || id;

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

                setNews(response.data[0].data);
            } catch (error) {
                if(news.length === 0) {
                    navigate("/not-existing")
                }
                toast.error(`:( Troubles With This News Loading: ${error}`);
            }
        };

        fetchNews();
    }, []);

    useEffect(() => {
        (news?.title) ? setLoading(false)
            : setTimeout(() => {
                setLoading(false);
            }, 2000)
    }, [news]);

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
                            />
                        ))
                    }

                    <h4 className="date">{news?.timestamp}</h4>
                </>
                ) : (loading === false) ?
                    (
                        <div className={"noItems"}>
                            <h1>no such news was found :(</h1>
                        </div>
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