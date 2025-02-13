import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints.js";
import { toast } from "sonner";
import TeamCard from "../../components/cards/teamCard.jsx"
import SearchBlock from "../../components/containers/searchBlock.jsx";
import NoItems from "../../components/NoItems.js";
import Filters from "../../components/containers/filtersBlock.jsx";
import { RiArrowLeftWideLine } from "react-icons/ri";

function TeamPage() {
    const { leagueName } = useParams();

    const cardSizes = {
        large: { rows: 4, columns: 4, cardSize: { width: 280, height: 350 }, postsPerPage: 16 },
        medium: { rows: 5, columns: 5, cardSize: { width: 220, height: 280 }, postsPerPage: 25 },
        small: { rows: 10, columns: 2, cardSize: { width: 600, height: 100 }, postsPerPage: 20 }
    };

    const navigate = useNavigate();
    const location = useLocation();
    const stateData = location.state || {};
    const leagueId = stateData.leagueId;
    const sportId = stateData.sportId;

    const [currentTeams, setCurrentTeams] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [teamsPerPage, setTeamsPerPage] = useState(cardSizes.large.postsPerPage);
    const [gridSize, setGridSize] = useState(cardSizes.large);

    const [loading, setLoading] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [prevInputValue, setPrevInputValue] = useState('');
    const [searchClicked, setSearchClicked] = useState(false);
    const [passedPosts, setPassedPosts] = useState(0);

    useEffect(() => {
        let page = Math.floor(passedPosts / teamsPerPage);
        setCurrentPage(page);
        getTeams(page);
    }, [teamsPerPage]);

    const handleGridSizeChange = (size) => {
        console.log('size: ', size);
        if (cardSizes[size]) {
            setPassedPosts(gridSize.rows * gridSize.columns * currentPage);
            setTeamsPerPage(cardSizes[size].postsPerPage);
            setGridSize(cardSizes[size]);
        } else {
            setGridSize(cardSizes.large);
        }
    };

    useEffect(() => {
        getTeams(0);
    }, []);

    const handlePageClick = (event) => {
        const selectedPage = event.selected;
        setCurrentPage(selectedPage);
        getTeams(selectedPage);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    function handleSearchClick() {
        setSearchClicked((prev) => !prev);
    }

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSearchClick();
        }
    };

    const getTeams = async (page) => {

        setPrevInputValue(inputValue);

        try {
            setLoading(true);

            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.teams.getAll}`,
                {
                    teams__sport_id: sportId,
                    leagues__league_id: leagueId,
                    page: page + 1,
                    per_page: teamsPerPage
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentTeams(response.data.teams);
            console.log(response.data.teams);
            const totalPosts = response.data.count;
            setPageCount(Math.ceil(totalPosts / teamsPerPage));
        } catch (error) {
            setPageCount(0);
            toast.error(`:( Troubles With Leagues Loading: ${error}`);
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
                (currentTeams.length > 0) ? setLoading(false)
                    : setTimeout(() => {
                        setLoading(false);
                    }, 2000)
            )
    }, [loading]);

    return (
        <div className="leagues-page">

            <div className="title">
                <button className="filled arrow" onClick={() => navigate(-1)}><RiArrowLeftWideLine className="arrow" /></button>
                <h1>{leagueName} teams</h1>
            </div>
            <Filters></Filters>

            {!(currentTeams.length === 0) ?
                <SearchBlock
                    cardSizes={cardSizes}
                    gridSize={gridSize}
                    postsPerPage={teamsPerPage}
                    onGridSizeChange={handleGridSizeChange}
                    pageCount={pageCount}
                    currentPage={currentPage}
                    onPageChange={handlePageClick}
                    loading={loading}
                    paginationKey={paginationKey}
                    children={currentTeams.map((item) => (
                        <TeamCard
                            leagueName={item.name}
                            img={item.logo}
                            sport={item.sport}
                            id={item.id}
                        />
                    ))}>
                </SearchBlock> : <NoItems text='No teams were found' />}
        </div>
    );
}

export default TeamPage;