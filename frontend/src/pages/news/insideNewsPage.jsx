import React, { useState, useEffect, useRef, useContext } from "react";
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { FaRegHeart, FaHeart } from "react-icons/fa";
import { VscEye } from "react-icons/vsc";
import axios from "axios";
import {toast} from "sonner";
import globalVariables from "../../globalVariables";
import apiEndpoints from "../../apiEndpoints";
import { AuthContext } from "../registration/AuthContext"
import useTranslations from "../../translationsContext";
import { useInteractionTypes } from "../../interactionContext";

export default function InsideNewsPage() {
    const { t } = useTranslations();
    const navigate = useNavigate();
    const { articleId } = useParams();
    const location = useLocation();
    const newsData = location.state?.newsData;
    const [article, setArticle] = useState()
    const [likes, setLikes] = useState()
    const [sections, setSections] = useState()
    const [views, setViews] = useState()
    const [likeStatus, setLikeStatus] = useState(false);
    const [initialLikeStatus, setInitialLikeStatus] = useState(false);
    const elementRef = useRef(null);
    const [hasRead, setHasRead] = useState(false);
    const likeStatusRef = useRef(likeStatus);
    const initialLikeStatusRef = useRef(initialLikeStatus);
    const { user } = useContext(AuthContext)
    const interactionTypes = useInteractionTypes();

    useEffect(() => {
        return () => {
          handleLikeStatus();
        };
      }, []);

    const [user_id, setUserId] = useState(() => {
        const savedUserId = localStorage.getItem('user_id');
        return savedUserId ? savedUserId : user?.user_id; 
    });

    useEffect(() => {
        if (user && user.user_id) {
            localStorage.setItem('user_id', user.user_id);
            setUserId(user.user_id); 
        }
    }, [user]); 

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
                    navigate(globalVariables.routeLinks.nonExistingRoute);
                });
        } else {
            setArticle(newsData?.article);
        }
    }, []);

    useEffect(() => {
        if(article) setSections(Object.values(article?.article))
    }, [article]);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting && !hasRead) {
                    saveInteraction(interactionTypes.READ);
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
        const handleEvent = (e) => {
            e.preventDefault();
            e.returnValue = ''; 
            handleLikeStatus();
        };

        window.addEventListener("beforeunload", handleEvent);

        return () => {
            window.removeEventListener("beforeunload", handleEvent);
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
            let interactionType = likeStatusRef.current ? interactionTypes.LIKE : interactionTypes.DISLIKE;
            saveInteraction(interactionType);
        }
    };

    useEffect(() => {
        const logInteraction = async () => {
            await saveInteraction(interactionTypes.OPEN);
        };
        logInteraction();
    }, []);

    const saveInteraction = async (interactionType) => {
        if (user_id) {
            try {
                await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.interactions.save}`,
                    {
                        user_id: user_id,
                        article_blob_id: articleId,
                        interaction_type: interactionType,
                    }
                );
            } catch (error) {
                toast.error(`Failed to save interaction: ${error}`)
            }
        }
    };

    useEffect(() => {
        async function getInteractionsCounts() {
            try {
                const { data } = await axios.get(`${apiEndpoints.url}${apiEndpoints.interactions.getCounts}`, {
                    params: {
                        article_blob_id: articleId,
                    },
                });
                setLikes(data.likes);
                setViews(data.views);
            }
            catch (error) {
                toast.error(`Failed to get interactions counts: ${error}`)
            }
        }
        getInteractionsCounts()
    }, [] );

    useEffect(() => {
        async function getLikeStatus() {
            try {
                const { data } = await axios.get(`${apiEndpoints.url}${apiEndpoints.interactions.getStatus}`, {
                    params: {
                        user_id: user.user_id,
                        article_blob_id: articleId,
                        interaction_type: interactionTypes.LIKE
                    },
                });
                setLikeStatus(data);
                setInitialLikeStatus(data);
            } catch (error) {
                toast.error(`Failed to get like status: ${error}`)
            }
        }

        if (user && articleId) {
            getLikeStatus();
        }
    }, [user, articleId]);

    const toggleLike = () => {
        if (user) {
            setLikeStatus(prev => {
                const newStatus = !prev;
                setLikes(count => newStatus ? count + 1 : count - 1);
                return newStatus;
            });
        }
        else {
            const notify = () => toast('Sign in to like this post', {
                action: {
                    label: 'sign in',
                    onClick: () =>  navigate(globalVariables.routeLinks.signInRoute) ,
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

            {article?.images[0] ? <img src={article?.images[0]}/> : null}

            <section className="content" ref={elementRef}>

                {
                    sections &&
                        sections.map((item, index) => (
                            <section className={"article-section"} key={index}>
                                {item?.subheadings.length > 0 ? <h3>{item?.subheadings[index]}</h3> : null}
                                {index > 0 && article?.images[index] ? <img src={article?.images[index]}/> : null}
                                <p>{item?.content}</p>
                                <br/>
                            </section>
                        ))
                }
            </section>

            <div className="details">
                <div className="date">{article?.timestamp}</div>
                <div className="views">
                    <VscEye />{views}
                </div>
                <button className="like-vrapper" onClick={toggleLike}>
                    <div className="like-content">
                        {likeStatus ? <FaHeart /> : <FaRegHeart />}{likes}
                    </div>
                </button>
            </div>

            <section className="comments">
            
                <hr />
               
            </section>
        </section>
    );
}