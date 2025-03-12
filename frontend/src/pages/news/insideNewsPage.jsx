import React, { useState, useEffect, useRef } from "react";
import img1 from '../imgs/1.jpg'
import { FaRegHeart } from "react-icons/fa";
import { FaHeart } from "react-icons/fa";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";

export default function InsideNewsPage() {
    const newsId = 1
    const title = 'Metallum Nostrum'
    const sport = 'Football'
    const date = '2025-01-23'
    const likes = 10
    const content = 'Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler'

    const userId = 1;
    const [loginStatus, setLoginStatus] = useState(true);
    const [likeStatus, setLikeStatus] = useState(false);
    const [initialLikeStatus, setInitialLikeStatus] = useState(false);

    const [isVisible, setIsVisible] = useState(false);
    const elementRef = useRef(null);

    const [hasRead, setHasRead] = useState(false);

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
        const handleBeforeUnload = (event) => {
            handleLikeStatus();
        };
        const handlePopState = () => {
            handleLikeStatus();
        };

        window.addEventListener("beforeunload", handleBeforeUnload);
        window.addEventListener("popstate", handlePopState);

        return () => {
            window.removeEventListener("beforeunload", handleBeforeUnload);
            window.removeEventListener("popstate", handlePopState);
        };
    }, []);

    const likeStatusRef = useRef(likeStatus);
    const initialLikeStatusRef = useRef(initialLikeStatus);

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
        try {
            await axios.post(
                `${apiEndpoints.url}${apiEndpoints.interactions.saveInteraction}`,
                {
                    user_id: userId,
                    news_id: newsId,
                    type_of_interaction: interactionType,
                    //time++
                }
            );
        } catch (error) {
            console.error("Error with interaction:", error);
        }
    };

    useEffect(() => {
        async function getLikeStatus() {
            try {
                const { data } = await axios.get(`${apiEndpoints.url}${apiEndpoints.interactions.getLikeStatus}`, {
                    params: {
                        user_id: userId,
                        news_id: newsId,
                    },
                });
                setLikeStatus(data.status);
                setInitialLikeStatus(data.status);
            } catch (error) {
                console.error("Error fetching like status:", error);
            }
        }

        if (loginStatus && newsId) {
            getLikeStatus();
        }
    }, [loginStatus, newsId]);


    const toggleLike = () => {
        if (!loginStatus) {
            return;
        }
        console.log('hello????')
        setLikeStatus(prev => {
            return !prev;
        });
    };

    return (
        <section className="news-block">
            <h1>{title}</h1>

            <div className="tags">
                <p>Tags:</p>
                <span className="tag">{sport}</span>
            </div>

            <img src={img1} alt={title} />

            <section className="content" ref={elementRef}>
                {content}
            </section>

            <div className="details">
                <div className="date">{date}</div>
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