import React, { useState, useEffect, useRef, useContext } from "react";
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { FaRegHeart, FaHeart } from "react-icons/fa";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { AuthContext } from "../registration/AuthContext"
import { toast } from "sonner";
import useTranslations from "../../translationsContext";

export default function InsideNewsPage() {

    const { t } = useTranslations();
    const navigate = useNavigate();
    const { articleId } = useParams();
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
                    console.log("response",{response})
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
        if (article) setSections(Object.values(article?.article))
    }, [article]);

    const [likeStatus, setLikeStatus] = useState(false);
    const [initialLikeStatus, setInitialLikeStatus] = useState(false);
    const elementRef = useRef(null);
    const [hasRead, setHasRead] = useState(false);
    const likeStatusRef = useRef(likeStatus);
    const initialLikeStatusRef = useRef(initialLikeStatus);

    const { user } = useContext(AuthContext)


    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting && !hasRead) {
                    saveInteraction('read');
                    setHasRead(true);
                }
            },
            { threshold: 0.8 }
        );

        if (elementRef.current) {
            observer.observe(elementRef.current);
        }

        return () => {
            if (elementRef.current) {
                observer.unobserve(elementRef.current);
            }
        };
    }, [hasRead]);

    useEffect(() => {
        const handleEvent = () => {
            handleLikeStatus();
        };

        window.addEventListener("beforeunload", handleEvent);
        window.addEventListener("popstate", handleEvent);

        return () => {
            window.removeEventListener("beforeunload", handleEvent);
            window.removeEventListener("popstate", handleEvent);
        };
    }, []);

    useEffect(() => {
        initialLikeStatusRef.current = initialLikeStatus;
    }, [initialLikeStatus]);

    useEffect(() => {
        likeStatusRef.current = likeStatus;
    }, [likeStatus]);

    const handleLikeStatus = async () => {
        if (likeStatusRef.current !== initialLikeStatusRef.current) {
            let interactionType = likeStatusRef.current ? 'like' : 'dislike';
            saveInteraction(interactionType);
        }
    };

    useEffect(() => {
        const logInteraction = async () => {
            await saveInteraction('open');
        };
        logInteraction();
    }, []);

    const saveInteraction = async (interactionType) => {
        if (user) {
            try {
                await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.interactions.saveInteraction}`,
                    {
                        user_id: user.id,
                        news_id: articleId,
                        interaction_type: interactionType,
                        timestamp: new Date().toISOString(),
                    }
                );
            } catch (error) {
                toast.error(`Troubles with saving interaction: ${error}`)
            }
        }
    };

    useEffect(() => {
        async function getLikeStatus() {
            try {
                const { data } = await axios.get(`${apiEndpoints.url}${apiEndpoints.interactions.getInteractionStatus}`, {
                    params: {
                        user_id: user.id,
                        news_id: articleId,
                        interaction_type: 'like'
                    },
                });
                setLikeStatus(data.status);
                setInitialLikeStatus(data.status);
            } catch (error) {
                toast.error(`Troubles with getting like status: ${error}`)
            }
        }

        if (user && articleId) {
            getLikeStatus();
        }
    }, [user, articleId]);

    const toggleLike = () => {
        if (user) {
            setLikeStatus(prev => {
                return !prev;
            });
        }
        else {
            const notify = () => toast('Sign in to leave your reaction', {
                action: {
                    label: 'sign in',
                    onClick: () => window.location.href = '/sign-in',
                },
            });
            notify()
        }
    };
    return (
        <section className="news-block">

            <h1>{article?.title}</h1>

            <div className="tags">
                <p>{t("tags")}</p>
                <span className="tag">{article?.S_P_O_R_T}</span>
            </div>

            {article?.images[0] ? <img src={article?.images[0]} /> : null}

            <section className="content" ref={elementRef}>

                {
                    sections ?
                        sections.map((item, index) => (
                            <React.Fragment key={index}>
                                {item?.subheadings.length > 0 ? <h3>{item?.subheadings[index]}</h3> : null}
                                {index > 0 && article?.images[index] ? <img src={article?.images[index]} /> : null}
                                <p>{item?.content}</p>
                                <br />
                            </React.Fragment>
                        )) : null
                }
            </section>

            <div className="details">
                <div className="date">{article?.timestamp}</div>
                <button className="like-vrapper" onClick={toggleLike}>
                    <div className="like-content">
                        {likeStatus ? <FaHeart /> : <FaRegHeart />} {likes}
                    </div>
                </button>
            </div>

            <section className="comments">

                <hr />

            </section>
        </section>
    );
}