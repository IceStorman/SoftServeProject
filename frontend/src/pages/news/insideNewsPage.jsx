import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from 'react-router-dom';
import { FaRegHeart } from "react-icons/fa";
import useTranslations from "../../translationsContext";
import apiEndpoints from "../../apiEndpoints";
import axios from "axios";
import {toast} from "sonner";
import CommentsBlock from "../../components/containers/commentsBlock";


export default function InsideNewsPage() {
    const { t } = useTranslations();
    const navigate = useNavigate();
    const {articleId} = useParams();
    const location = useLocation();
    const newsData = location.state?.newsData;
    const [article, setArticle] = useState()
    const [likes, setLikes] = useState()
    const [sections, setSections] = useState()

    useEffect(() => {
        if (!newsData) {
            axios
                .post(
                    `${apiEndpoints.url}${apiEndpoints.news.getArticle}`,
                    { blob_id: articleId },
                    { headers: { 'Content-Type': 'application/json' } }
                )
                .then((response) => {
                    setArticle(response?.data[0]?.data);
                })
                .catch((error) => {
                    toast.error(`:( Trouble loading news: ${error}`);
                    navigate("/not-existing");
                });
        } else {
            setArticle(newsData?.article);
            setLikes(newsData?.likes);
        }
    }, []);

    useEffect(() => {
        if(article) setSections(Object.values(article?.article))
    }, [article]);

    const [comments, setComments] = useState([])

    const fetchComments = async () => {
        try {
            const response = await axios.get(
                `${apiEndpoints.url}${apiEndpoints.comment.getComments}`, {
                params:
                    { article_blob_id: articleId },
            }
            );
            console.log("comments:", {response})
            setComments(response.data);
        } catch (error) {
            console.error("Error fetching replies:", error);
        }
    };

    useEffect(()=>{
        fetchComments()
    }, []);

    return (
        <section className="news-block">

            <h1>{article?.title}</h1>

            <div className="tags">
                <p>{t("tags")}</p>
                <span className="tag">{article?.S_P_O_R_T}</span>
            </div>

            {article?.images[0] ? <img src={article?.images[0]}/> : null}

            <section className="content">

                {
                    sections ?
                        sections.map((item, index) => (
                            <React.Fragment key={index}>
                                {item?.subheadings.length > 0 ? <h3>{item?.subheadings[index]}</h3> : null}
                                {index > 0 && article?.images[index] ? <img src={article?.images[index]}/> : null}
                                <p>{item?.content}</p>
                                <br/>
                            </React.Fragment>
                        )) : null
                }
            </section>

            <div className="details">
            <div className="date">{article?.timestamp}</div>
                <button className="like-vrapper">
                    <div className="like-content">
                    <FaRegHeart /> {likes}
                    </div>
                </button>
            </div>

            <section className="comments">
            
                <CommentsBlock comments={comments} />
               
            </section>
        </section>
    );
}