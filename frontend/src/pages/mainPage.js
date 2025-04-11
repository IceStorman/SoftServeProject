import React, {useState, useEffect, useRef, useContext} from "react";
import axios from 'axios';
import apiEndpoints from "../apiEndpoints";
import { toast } from "sonner";
import NoItems from "../components/NoItems";
import { NavLink } from "react-router-dom";
import NewsCard from "../components/cards/newsCard.jsx";
import NewsShowcase from "../components/containers/newsShowcase.jsx";
import Column from "../components/containers/column.jsx";
import GameSlider from "../components/containers/gameSlider.jsx";
import GameCard from "../components/cards/gameCard.jsx"
import GridContainer from "../components/containers/gridBlock.jsx";
import useTranslations from "../translationsContext";
import {AuthContext} from "./registration/AuthContext";
import GridRecommendationBlock from "../components/containers/gridRecommendationBlock";
import globalVariables from "../globalVariables";


function MainPage() {
    const { user } = useContext(AuthContext);
    const [loading, setLoading] = useState(false)
    const [sports, setSport] = useState([]);
    const { t } = useTranslations();
    const [news, setNews] = useState([])
    const [newsPaginated, setNewsPaginated] = useState([])

    const game_element_height = 85
    const game_element_width = 400

    const cardSizes = {
        large: { rows: 1, columns: 4, cardSize: { width: 320, height: 490 }, postsPerPage: 4 },
        medium: { rows: 3, columns: 5, cardSize: { width: 250, height: 300 }, postsPerPage: 10 },
        small: { rows: 5, columns: 2, cardSize: { width: 650, height: 100 }, postsPerPage: 8 }
    };

    const [gridSize, setGridSize] = useState(cardSizes.large);

    const [preferenceNewsGridSize, setPreferenceNewsGridSize] = useState(cardSizes.large);
    const [newsGridSize, setNewsGridSize] = useState(cardSizes.large);
    const [lastWatchNewsGridSize, setLastWatchNewsGridSize] = useState(cardSizes.large);

    const [orderValue, setOrderValue] = useState("desc")
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [postsPerPage, setPostsPerPage] = useState(cardSizes.large.postsPerPage);

    const newsRef = useRef(null);

    const scrollToTarget = () => {
        newsRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.sports.getAll}`)
            .then(res => {
                const returnedSports = res.data;
                setSport(returnedSports);
            })
            .catch(error => {
                toast.error(`Troubles With Sports Loading: ${error}`);
            });
    }, []);

    useEffect(() => {
        axios.get(`${apiEndpoints.url}${apiEndpoints.news.getRecent}`)
            .then(res => {
                const returnedNews = res.data;
                setNews(returnedNews);
            })
            .catch(error => {
                toast.error(`There was an error getting news :( ${error}`);
            });
    }, []);

    useEffect(() => {
        getPaginatedNews(0)
        setCurrentPage(0)
    }, [newsGridSize, orderValue]);

    const getPaginatedNews = async (page) => {

        try {
            setLoading(true);
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.news.getPaginated}`,
                {
                    pagination: {
                        page: page + 1,
                        per_page: postsPerPage,
                    },
                    filters:[
                        {
                            filter_name: "news",
                            order_field: "save_at",
                            order_type: orderValue
                        }
                    ]
                },
                { headers: { 'Content-Type': 'application/json' }, }
            );

            setNewsPaginated(response.data.items);
            setPageCount(response.data.count / postsPerPage)
        } catch (error) {
            setPageCount(0);
            toast.error(`Troubles With games Loading: ${error}`);
        }
    };

    const [currentGames, setCurrentGames] = useState([]);
    // const [slidesCount, setSlidesCount] = useState(0);
    // const [currentSlide, setCurrentSlide] = useState(0);
    const [gamesPerSlide, setGamesPerSlide] = useState(5);
    const [recommendationNews, setRecommendationNews] = useState([]);


    useEffect(() => {
        getGames(0);
    }, []);
    //
    // const handleSliderClick = (event) => {
    //     const selectedSlide = event.selected;
    //     setCurrentSlide(selectedSlide);
    //     getGames(selectedSlide);
    // };

    const getGames = async (page) => {

        const today = new Date();
        const formattedDate = today.toISOString().split('T')[0];

        const filtersData = [
            { 'filter_name': 'date_from',  'filter_value': formattedDate},
            { 'filter_name': 'date_to',  'filter_value': formattedDate},
        ]

        try {
            setLoading(true);
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.games.getGames}`,
                {
                    pagination: {
                        page: page + 1,
                        per_page: gamesPerSlide,
                    },
                    filters: filtersData
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentGames(response.data.items);
            // const totalGames = response.data.count;
            // setSlidesCount(Math.ceil(totalGames / gamesPerSlide));
        } catch (error) {
            setPageCount(0);
            toast.error(`Troubles With games Loading: ${error}`);
        }
    };

    useEffect(() => {
        try {
            if (!user) return;

            axios.get(`${apiEndpoints.url}${apiEndpoints.news.getRecommendations}`,
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true
                })
                .then(res => {
                    setRecommendationNews(res.data);
                })
                .catch(error => {
                    toast.error(`:( Troubles With Recommendation News Loading: ${error}`);
                })

        } catch (error) {
            toast.error(`Error parsing user cookie:", ${error}`);
        }

    }, [user]);

    const handleGridSizeChange = (size) => {
        if (cardSizes[size]) {
            setPostsPerPage(cardSizes[size].postsPerPage);
            setNewsGridSize(cardSizes[size]);
        } else {
            setNewsGridSize(cardSizes.large);
        }
    };

    const handlePageClick = (event) => {
        const selectedPage = event.selected;
        setCurrentPage(selectedPage);
        getPaginatedNews(selectedPage);
    };

    const [selectedSport, setSelectedSport] = useState("all");
    const element_height = 100
    const element_width = 350
    return (
        <>
            <div className="showcase">
                <section>
                    <p className="block-title">Latest news</p>
                    <div className="news-column">
                        <Column>
                            {news.map((item, index) => (
                                <NewsCard
                                    key={index}
                                    title={item?.data?.title}
                                    date={item?.data?.timestamp}
                                    img={item?.data?.images[0] || null}
                                    sport={item?.data?.S_P_O_R_T}
                                    content={item?.data?.article?.section_1?.content}
                                    id={item?.blob_id}
                                    article={item?.data}
                                    height={element_height}
                                    width={element_width}
                                    className="news-card"
                                />
                                )
                            )}
                        </Column></div>
                    <button onClick={scrollToTarget} className="boxed">{t("more")}</button>
                </section>

                <NewsShowcase newsData={news} />

                <section>
                    <p className="block-title">{t("latest_games")}</p>
                    <div className="games-column">
                        <Column>
                            {
                                currentGames.map((item, index) => (
                                    <GameCard
                                        key={index}
                                        nameHome={item.home_team_name}
                                        nameAway={item.away_team_name}
                                        logoHome={item.home_team_logo}
                                        logoAway={item.away_team_logo}
                                        scoreHome={item.home_score}
                                        scoreAway={item.away_score}
                                        time={item.time}
                                        isVertical={false}
                                    />
                                ))
                            }
                        </Column>
                    </div>

                    {
                        !user ? (
                            <div className="blue-placeholder">
                                <h1><NavLink to={globalVariables.routeLinks.signInRoute} className="nav-link" activeClassName="active">{t("sign_up_to")}</NavLink> {t("follow_teams")}</h1>
                            </div>
                        ) : null
                    }

                </section>
            </div>

            {
                user ? (
                    <>
                        {recommendationNews.recommendations_list_by_user_preferences && recommendationNews.recommendations_list_by_user_preferences.length > 0 && (
                            <GridRecommendationBlock
                                title={t("recommend_pref")}
                                gridSize={preferenceNewsGridSize}
                                onGridSizeChange={(size) => handleGridSizeChange(setPreferenceNewsGridSize, size)}
                            >
                                {recommendationNews.recommendations_list_by_user_preferences.map((item) => (
                                    <NewsCard
                                        key={item?.news_id}
                                        title={item?.article?.title}
                                        id={item?.news_id}
                                        date={item?.article?.timestamp}
                                        img={item?.article?.images[0] || ''}
                                        sport={item?.article?.S_P_O_R_T}
                                        content={item?.article?.article?.section_1?.content}
                                        article={item?.article}
                                    />
                                ))}
                            </GridRecommendationBlock>
                        )}
                    </>
                ) : null
            }


            <section className="game-slider-showcase">
                <div className="sport-options">
                    <button type="button"
                        className={selectedSport === "all" ? "active" : ""}
                        onClick={() => setSelectedSport("all")}>
                        {t('all')}
                    </button>
                    {!(sports.length === 0) ?
                        sports.map((item, index) => (
                            <button
                                key={index}
                                type="button"
                                className={selectedSport === item.id ? "active" : ""}
                                onClick={() => setSelectedSport(item.id)}
                            >
                                {item.sport}
                            </button>
                        ))
                        : (loading === false) ?
                            (
                                <NoItems
                                    key={1}
                                    text={t("news_not_found")}
                                />
                            ) : null
                    }
                </div>
                <div className="games-slider-outer">
                    <GameSlider sportId={selectedSport} />
                </div>
            </section>

            <div ref={newsRef}>
                <GridContainer
                    title={t("news")}
                    cardSizes={cardSizes}
                    gridSize={newsGridSize}
                    postsPerPage={postsPerPage}
                    onGridSizeChange={(size) => handleGridSizeChange(size)}
                    pageCount={pageCount}
                    currentPage={currentPage}
                    onPageChange={handlePageClick}
                    loading={loading}
                    setSortValue={setOrderValue}
                    children={newsPaginated.map((item, index) => (
                        <NewsCard
                            key={index?.blob_id}
                            title={item?.data?.title}
                            date={item?.data?.timestamp}
                            img={item?.data?.images[0] || null}
                            sport={item?.data?.S_P_O_R_T}
                            content={item?.data?.article?.section_1?.content}
                            id={item?.blob_id}
                            article={item?.data}
                        />
                    ))}>
                </GridContainer ></div>

            {
                user ? (
                    <>
                        {recommendationNews.recommendations_list_by_user_last_watch && recommendationNews.recommendations_list_by_user_last_watch.length > 0 && (
                            <GridRecommendationBlock
                                title={t("recommend_watch")}
                                gridSize={lastWatchNewsGridSize}
                                onGridSizeChange={(size) => handleGridSizeChange(setLastWatchNewsGridSize, size)}
                            >
                                {recommendationNews.recommendations_list_by_user_last_watch.map((item) => (
                                    <NewsCard
                                        key={item?.news_id}
                                        title={item?.article?.title}
                                        id={item?.news_id}
                                        date={item?.timestamp}
                                        img={item?.article?.images[0] || ''}
                                        sport={item?.article?.S_P_O_R_T}
                                        content={item?.article?.article?.section_1?.content}
                                        article={item?.article}
                                    />
                                ))}
                            </GridRecommendationBlock>
                        )}
                    </>
                ) : null
            }
        </>
    );
}

export default MainPage;