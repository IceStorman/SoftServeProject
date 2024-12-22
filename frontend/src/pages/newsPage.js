import React, {useEffect, useState} from "react";
import {useLocation} from "react-router-dom";
import NewsSection from "../components/newsPage/newsSection";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";

function NewsPage(){
    const location = useLocation();
    const newsId = location.state || {};

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
                        ))}

                    <h4 className="date">{news?.timestamp}</h4>
                </>
            ) : null}

        </section>

    );
}

export default NewsPage;