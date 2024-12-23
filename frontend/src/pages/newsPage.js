import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import NewsSection from "../components/newsPage/newsSection";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";

function NewsPage(){
    const {id} = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    console.log(id)
    const newsId = location.state || {id};

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

                setNews(response.data[0].data);
            } catch (error) {
                if(news.length === 0) {
                    navigate("/not-existing")
                }
                toast.error(`:( Troubles With This News Loading: ${error}`);
            } finally {
                setLoading(false);
            }
        };

        fetchNews();
    }, []);

    return(

        <section className={"newsContent"}>

            {!loading ? (
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
                ) :
                <div className="loader"></div>
            }

        </section>

    );
}

export default NewsPage;