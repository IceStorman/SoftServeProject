import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints.js";
import { toast } from "sonner";
import SearchBlock from "../../components/containers/searchBlock.jsx";
import LeagueCard from "../../components/cards/leagueCard"
import NoItems from "../../components/NoItems";
import Filters from "../../components/containers/filtersBlock.jsx";
import { RiArrowLeftWideLine } from "react-icons/ri";
import useTranslations from "../../translationsContext";

function LeaguePage() {
    const { sportName } = useParams();

    const navigate = useNavigate();

    const location = useLocation();
    const stateData = location.state || {};
    const sportId = stateData.sportId;

    const cardSizes = {
        large: { rows: 4, columns: 4, cardSize: { width: 280, height: 350 }, postsPerPage: 16 },
        medium: { rows: 5, columns: 5, cardSize: { width: 220, height: 280 }, postsPerPage: 25 },
        small: { rows: 10, columns: 2, cardSize: { width: 600, height: 100 }, postsPerPage: 20 }
    };

    const [currentLeagues, setCurrentLeagues] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [leaguesPerPage, setLeaguesPerPage] = useState(cardSizes.large.postsPerPage);
    const [gridSize, setGridSize] = useState(cardSizes.large);
    const [passedPosts, setPassedPosts] = useState(0);
    const { t } = useTranslations();


    useEffect(() => {
        let page = Math.floor(passedPosts / leaguesPerPage);
        setCurrentPage(page);
        getLeagues(page);
    }, [leaguesPerPage]);

    const handleGridSizeChange = (size) => {
        console.log('size: ', size);
        if (cardSizes[size]) {
            setPassedPosts(gridSize.rows * gridSize.columns * currentPage);
            setLeaguesPerPage(cardSizes[size].postsPerPage);
            setGridSize(cardSizes[size]);
        } else {
            setGridSize(cardSizes.large);
        }
    };

    const [loading, setLoading] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [prevInputValue, setPrevInputValue] = useState('');
    const [searchClicked, setSearchClicked] = useState(false);

    const handlePageClick = (event) => {
        const selectedPage = event.selected;
        setCurrentPage(selectedPage);
        getLeagues(selectedPage);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    useEffect(() => {
        getLeagues(0);
    }, []);

    const getLeagues = async (page) => {

        setPrevInputValue(inputValue);

        try {
            setLoading(true);

            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.sports.getLeagueSearch}`,
                {
                    leagues__sport_id: sportId,
                    page: page + 1,
                    per_page: leaguesPerPage
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentLeagues(response.data.leagues);
            const totalPosts = response.data.count;
            setPageCount(Math.ceil(totalPosts / leaguesPerPage));
        } catch (error) {
            setPageCount(0);
            toast.error(`Troubles With Leagues Loading: ${error}`);
        }
    };

    useEffect(() => {
        if (prevInputValue !== inputValue) {
            handlePageClick({ selected: 0 });
            setPaginationKey((prevKey) => prevKey + 1);
        }
    }, [searchClicked]);

    useEffect(() => {
        (loading === false) ? setLoading(false) :
            (
                (currentLeagues.length > 0) ? setLoading(false)
                    : setTimeout(() => {
                        setLoading(false);
                    }, 2000)
            )
    }, [loading]);

    return (

        <div className="leagues-page">
            <div className="title">
                <button className="filled arrow" onClick={() => navigate(-1)}><RiArrowLeftWideLine className="arrow" /></button>
                <h1>{sportName} {t("leagues")}</h1>
            </div>
            <Filters></Filters>

            {!(currentLeagues.length === 0) ?
                <SearchBlock
                    cardSizes={cardSizes}
                    gridSize={gridSize}
                    postsPerPage={leaguesPerPage}
                    onGridSizeChange={handleGridSizeChange}
                    pageCount={pageCount}
                    currentPage={currentPage}
                    onPageChange={handlePageClick}
                    loading={loading}
                    paginationKey={paginationKey}
                    children={currentLeagues.map((item) => (
                        <LeagueCard
                            leagueName={item.name}
                            img={item.logo}
                            sport={item.sport}
                            id={item.id}
                            sportId={sportId}
                        />
                    ))}
                >
                </SearchBlock> : <NoItems text='No leagues were found' />}
        </div>
    );
}

export default LeaguePage;