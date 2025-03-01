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
import img1 from "./imgs/1.jpg"
import img2 from "./imgs/2.jpg"
import img3 from "./imgs/3.jpg"
import img4 from "./imgs/4.jpg"
import img5 from "./imgs/5.jpg"
import GridContainer from "../components/containers/gridBlock.jsx";
import useTranslations from "../translationsContext";
import {AuthContext} from "./registration/AuthContext";
import Cookies from "js-cookie";

function MainPage() {
    const { user } = useContext(AuthContext);
    const [loading, setLoading] = useState(false)
    const [sports, setSport] = useState([]);
    const { t } = useTranslations();

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

    const [currentGames, setCurrentGames] = useState([]);
    const [slidesCount, setSlidesCount] = useState(0);
    const [currentSlide, setCurrentSlide] = useState(0);
    const [gamesPerSlide, setGamesPerSlide] = useState(6);
    const [recommendationNews, setRecommendationNews] = useState([]);


    useEffect(() => {
        getGames(0);
    }, []);

    const handleSliderClick = (event) => {
        const selectedSlide = event.selected;
        setCurrentSlide(selectedSlide);
        getGames(selectedSlide);
    };

    const getGames = async (page) => {
        try {
            setLoading(true);
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.games.getGame}`,
                {
                    page: page + 1,
                    per_page: gamesPerSlide
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );
            setCurrentGames(response.data.games);
            const totalGames = response.data.count;
            setSlidesCount(Math.ceil(totalGames / gamesPerSlide));
        } catch (error) {
            setPageCount(0);
            toast.error(`Troubles With games Loading: ${error}`);
        }
    };

    useEffect(() => {
        try {
            if (!user?.email) return;

            setLoading(true);

            axios.post(`${apiEndpoints.url}${apiEndpoints.news.getRecommendations}`,
                {
                    email: user.email,
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                })
                .then(res => {
                    console.log(res.data);
                    setRecommendationNews(res.data);

                })
                .catch(error => {
                    toast.error(`:( Troubles With Recommendation News Loading: ${error}`);
                })

        } catch (error) {
            toast.error(`Error parsing user cookie:", ${error}`);
        }

    }, [user]);

    const testNews = [
        {
            title: 'Metallum Nostrum',
            date: '2025-01-23',
            img: img1,
            sport: 'Football',
            id: '1',
            content: 'Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler'
        },
        {
            title: 'Bible of the Beast',
            date: '2025-01-23',
            img: img3,
            sport: 'NBA',
            id: '3',
            content: 'Resurrection by erection Raise your phallus to the sky and you never die It\'s resurrection by erection Raise your bone up to the sky and you\'re never gonna die Hallelujah, resurrection'
        },
        {
            title: 'Preachers of the Night',
            date: '2025-01-23',
            img: img4,
            sport: 'AAAAAAAAA',
            id: '4',
            content: 'Bring me pandemonium Speak the word of God All we need in life is flesh and blood Bring me sanctimonium Armageddon flood All we care is how to get more blood'
        },
        {
            title: 'Wake up the Wiked',
            date: '2025-01-23',
            img: img2,
            sport: 'Baseball',
            id: '2',
            content: 'Sails in the wind and the word of God in mind Hailed by the sin left our morals all behind Blessed by the crown and to shores ahead we ride Trails in the waves by the cross we are allied Christ in our hearts but for mercy we are blind Restless and damned we are knights of sacred might We fight the Bible by our side'
        },
        {
            title: 'Call of the Wild',
            date: '2025-01-23',
            img: img5,
            sport: 'hello?',
            id: '5',
            content: 'Forced to believе that the Heavens strike back Lined up to die in despair One-by-one torn to dust and all sworn to the black Signed up and ready to swear God given Sermon of swords bring sancted fire Sermon of swords, wake up Messiah Sermon of swords, we raise the pyre All we can set the night on fire'
        },
        {
            title: 'Metallum Nostrum',
            date: '2025-01-23',
            img: img1,
            sport: 'Football',
            id: '1',
            content: 'Howling winds keep screaming around And the rain comes pouring down Doors are locked and bolted now As the thing crawls into town Straight out of hell One of a kind Stalking his victim Don t look behind you Night crawler Beware the beast in black Night crawler You know he s coming back Night crawler'
        },
        {
            title: 'Wake up the Wiked',
            date: '2025-01-23',
            img: img2,
            sport: 'Baseball',
            id: '2',
            content: 'Sails in the wind and the word of God in mind Hailed by the sin left our morals all behind Blessed by the crown and to shores ahead we ride Trails in the waves by the cross we are allied Christ in our hearts but for mercy we are blind Restless and damned we are knights of sacred might We fight the Bible by our side'
        },
        {
            title: 'Bible of the Beast',
            date: '2025-01-23',
            img: img3,
            sport: 'NBA',
            id: '3',
            content: 'Resurrection by erection Raise your phallus to the sky and you never die It\'s resurrection by erection Raise your bone up to the sky and you\'re never gonna die Hallelujah, resurrection'
        },
        {
            title: 'Preachers of the Night',
            date: '2025-01-23',
            img: img4,
            sport: 'AAAAAAAAA',
            id: '4',
            content: 'Bring me pandemonium Speak the word of God All we need in life is flesh and blood Bring me sanctimonium Armageddon flood All we care is how to get more blood'
        },
        {
            title: 'Call of the Wild',
            date: '2025-01-23',
            img: img5,
            sport: 'hello?',
            id: '5',
            content: 'Forced to believе that the Heavens strike back Lined up to die in despair One-by-one torn to dust and all sworn to the black Signed up and ready to swear God given Sermon of swords bring sancted fire Sermon of swords, wake up Messiah Sermon of swords, we raise the pyre All we can set the night on fire'
        }
    ]

    const game_element_height = 85
    const game_element_width = 400

    const cardSizes = {
        large: { rows: 1, columns: 4, cardSize: { width: 320, height: 490 }, postsPerPage: 4 },
        medium: { rows: 3, columns: 5, cardSize: { width: 250, height: 300 }, postsPerPage: 18 },
        small: { rows: 5, columns: 2, cardSize: { width: 650, height: 100 }, postsPerPage: 10 }
    };

    const testGames1 =
    {
        category1: [{
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            time: "01/12/25"
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },],

        category2: [{
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            time: "01/12/25"
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },
        {
            nameHome: "team1",
            nameAway: "team2",
            logoHome: img1,
            logoAway: img2,
            scoreHome: 1,
            scoreAway: 3,
        },]
    }

    const [gridSize, setGridSize] = useState(cardSizes.large);
    const [currentNews, setCurrentNews] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [postsPerPage, setPostsPerPage] = useState(cardSizes.large.postsPerPage);
    const [passedPosts, setPassedPosts] = useState(0);

    useEffect(() => {
        let page = Math.floor(passedPosts / postsPerPage);
        setCurrentPage(page);
        getNews(page);
    }, [postsPerPage]);

    const handleGridSizeChange = (size) => {
        console.log('size: ', size);
        if (cardSizes[size]) {
            setPassedPosts(gridSize.rows * gridSize.columns * currentPage);
            setPostsPerPage(cardSizes[size].postsPerPage);
            setGridSize(cardSizes[size]);
        } else {
            setGridSize(cardSizes.large);
        }
    };
    useEffect(() => {
        getNews(0);
    }, []);

    const handlePageClick = (event) => {
        const selectedPage = event.selected;
        setCurrentPage(selectedPage);
        getNews(selectedPage);
    };

    const getNews = (page) => {
        try {
            const slicedNews = testNews.slice(page * postsPerPage, (page + 1) * postsPerPage);
            setCurrentNews(slicedNews);
            const totalPosts = testNews.length;
            setPageCount(Math.ceil(totalPosts / postsPerPage));

        } catch (error) {
            setPageCount(0);
            toast.error(`:( Troubles With Leagues Loading: ${error}`);
        }
    };
    const [selectedSport, setSelectedSport] = useState("all");
    const showcaseGames = currentGames.slice(0, 5)
    const element_height = 100
    const element_width = 350
    return (
        <>
            <div className="showcase">
                <section>
                    <p className="block-title">Latest news</p>
                    <div className="news-column">
                        <Column>
                            {testNews.slice(0, 5).map((item, index) => (
                                <NewsCard
                                    title={item.title}
                                    date={item.date}
                                    img={item.img}
                                    sport={item.sport}
                                    content={item.content}
                                    height={element_height}
                                    width={element_width}
                                    className="news-card"
                                />))}
                        </Column></div>
                    <button onClick={scrollToTarget} className="boxed">{t("more")}</button>
                </section>

                <NewsShowcase newsData={testNews.slice(0, 5)} />

                <section>
                    <p className="block-title">{t("latest_games")}</p>
                    <div className="games-column">
                        <Column>
                            {
                                showcaseGames.map((item, index) => (
                                    <GameCard
                                        nameHome={item.home_team_name}
                                        nameAway={item.away_team_name}
                                        logoHome={item.home_team_logo}
                                        logoAway={item.away_team_logo}
                                        scoreHome={item.score_home_team}
                                        scoreAway={item.score_away_team}
                                        time={item.time}
                                        height={game_element_height }
                                        width={game_element_width}
                                    />
                                ))
                            }
                        </Column>
                    </div>

                    {
                        !user ? (
                            <div className="blue-placeholder">
                                <h1><NavLink to={"/sign-in"} className="nav-link" activeClassName="active">{t("sign_in")}</NavLink> {t("follow_teams")}</h1>
                            </div>
                        ) : null
                    }

                </section>
            </div>

            {
                user ? (
                    <>
                        {recommendationNews.recommendations_list_by_user_preferences && recommendationNews.recommendations_list_by_user_preferences.length > 0 && (
                            <GridContainer
                                title="Recommended news by your Preferences"
                                cardSizes={cardSizes}
                                gridSize={gridSize}
                                postsPerPage={postsPerPage}
                                onGridSizeChange={handleGridSizeChange}
                                pageCount={pageCount}
                                currentPage={currentPage}
                                onPageChange={handlePageClick}
                                loading={loading}
                                paginationKey={paginationKey}
                            >
                                {recommendationNews.recommendations_list_by_user_preferences.map((item) => (
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
                            </GridContainer>
                        )}
                    </>
                ) : null
            }


            <section className="game-slider-showcase">
                <div className="sport-options">
                    <button type="button"
                        className={selectedSport === "all" ? "active" : ""}
                        onClick={() => setSelectedSport("all")}>
                        All
                    </button>
                    {!(sports.length === 0) ?
                        sports.map((item, index) => (
                            <button
                                key={index}
                                type="button"
                                className={selectedSport === item.sport ? "active" : ""}
                                onClick={() => setSelectedSport(item.sport)}
                            >
                                {item.sport}
                            </button>
                        ))
                        : (loading === false) ?
                            (
                                <NoItems
                                    key={1}
                                    text={"No latest news were found"}
                                />
                            ) : null
                    }
                </div>
                <div className="games-slider-outer">
                    <GameSlider testGames1={testGames1}></GameSlider>
                </div>
            </section>

            <div ref={newsRef}>
                <GridContainer
                    title="News"
                    cardSizes={cardSizes}
                    gridSize={gridSize}
                    postsPerPage={postsPerPage}
                    onGridSizeChange={handleGridSizeChange}
                    pageCount={pageCount}
                    currentPage={currentPage}
                    onPageChange={handlePageClick}
                    loading={loading}
                    paginationKey={paginationKey}
                    children={currentNews.map((item) => (
                        <NewsCard
                            title={item.title}
                            date={item.date}
                            img={item.img}
                            sport={item.sport}
                            content={item.content}
                        />
                    ))}>
                </GridContainer ></div>

            {
                user ? (
                    <>
                        {recommendationNews.recommendations_list_by_user_last_watch && recommendationNews.recommendations_list_by_user_last_watch.length > 0 && (
                            <GridContainer
                                title="Recommended by your Last Watch"
                                cardSizes={cardSizes}
                                gridSize={gridSize}
                                postsPerPage={postsPerPage}
                                onGridSizeChange={handleGridSizeChange}
                                pageCount={pageCount}
                                currentPage={currentPage}
                                onPageChange={handlePageClick}
                                loading={loading}
                                paginationKey={paginationKey}
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
                            </GridContainer>
                        )}
                    </>
                ) : null
            }
        </>
    );
}

export default MainPage;