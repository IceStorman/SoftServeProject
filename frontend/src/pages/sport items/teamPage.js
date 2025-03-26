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
import useTranslations from "../../translationsContext";
import {FaFilter, FaTimes} from "react-icons/fa";
import FiltersRenderer from "../../components/filters/filterRender";
import globalVariables from "../../globalVariables";

function TeamPage() {
    const { leagueName } = useParams();

    const calculateColumns = (width, layout) => {
        if (width > globalVariables.windowsSizesForCards.desktopLarge) return layout.baseColumns;
        if (width > globalVariables.windowsSizesForCards.tablet) return Math.max(layout.baseColumns - 1, layout.minColumns);
        if (width > globalVariables.windowsSizesForCards.mobileLarge) {
            return layout.baseColumns === 4
                ? Math.max(layout.baseColumns - 1, layout.minColumns)
                : Math.max(layout.baseColumns - 1, layout.minColumns);
        }
        if (width < globalVariables.windowsSizesForCards.mobileSmall) {
            if (layout.baseColumns === 2) {
                return layout.minColumns - 1;
            }
        }
        return layout.minColumns;
    };

    const [gridSize, setGridSize] = useState({ ...globalVariables.cardLayouts.large, columns: calculateColumns(window.innerWidth, globalVariables.cardLayouts.large) });

    const calculateLeaguesPerPage = (layout) => {
        if (layout.minColumns === 1) return layout.alwaysColumns * 2;
        return gridSize.baseRows * gridSize.alwaysColumns
    }

    const [teamsPerPage, setTeamsPerPage] =  useState(calculateLeaguesPerPage(globalVariables.cardLayouts.large));

    useEffect(() => {
        setTeamsPerPage(gridSize.baseRows * gridSize.columns);
    }, [gridSize]);

    useEffect(() => {
        const handleResize = () => {
            setGridSize(prev => ({
                ...prev,
                columns: calculateColumns(window.innerWidth, prev)
            }));
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    const handleGridSizeChange = (size) => {
        if (globalVariables.cardLayouts[size]) {
            setGridSize({
                ...globalVariables.cardLayouts[size],
                columns: calculateColumns(window.innerWidth, globalVariables.cardLayouts[size])
            });
        }
    };

    const navigate = useNavigate();
    const location = useLocation();
    const stateData = location.state || {};
    const leagueId = stateData.leagueId;
    const sportId = stateData.sportId;
    const sportName = stateData.sportName;

    const [currentTeams, setCurrentTeams] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);

    const [loading, setLoading] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const [prevInputValue, setPrevInputValue] = useState('');
    const [searchClicked, setSearchClicked] = useState(false);
    const [passedPosts, setPassedPosts] = useState(0);
    const { t } = useTranslations();

    useEffect(() => {
        let page = Math.floor(passedPosts / teamsPerPage);
        setCurrentPage(page);
        getTeams(page);
    }, [teamsPerPage]);

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
            let response;

            if (sportName !== "formula-1" && sportName !== "mma") {

                const filtersData = [
                    ...filters,
                    { 'filter_name': 'sport_id', 'filter_value': sportId },
                    { 'filter_name': 'league_id', 'filter_value': leagueId }
                ];

                response = await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.teams.getTeamsAll}`,
                    {
                        sport_id: sportId,
                        league_id: leagueId,
                        filters_data: {
                            pagination: {
                                page: page + 1,
                                per_page: teamsPerPage,
                            },
                            filters: filtersData
                        }
                    },
                    {
                        headers: { 'Content-Type': 'application/json' },
                    }
                );
            }
            else {
                response = await axios.post(
                    `${apiEndpoints.url}${apiEndpoints.players.getPlayersAll}`,
                    {
                        sport_id: sportId,
                        team_id: leagueId,

                    },
                    {
                        headers: { 'Content-Type': 'application/json' },
                    }
                );
            }

            if (!response.data.items) {
                if (response.data.results === 0) {
                    setCurrentTeams([]);
                    setPageCount(0);
                    return;
                }
                return getTeams(0)
            }

            setCurrentTeams(response.data.items);
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

    const initialIcon = <FaFilter size={28} />

    const [selectedModel, setSelectedModel] = useState("teams");
    const [filters, setFilters] = useState([]);
    const [burgerMenu, setBurgerMenu] = useState(false)
    const [menuIsOpen, setMenuIsOpen] = useState(false)
    const [menuIcon, setMenuIcon] = useState(initialIcon)

    useEffect(() => {

        const handleResize = () => {
            const smallScreen = window.innerWidth <= globalVariables.windowSizeForBurger.filters
            setBurgerMenu(smallScreen)
        }

        handleResize();
        window.addEventListener("resize", handleResize);
    }, []);

    const handleOpenMenu = () => {
        setMenuIsOpen(prev => !prev)
        setMenuIcon(!menuIsOpen ? <FaTimes size={28} color="black" /> : initialIcon)
    }

    const handleFiltersChange = (newFilters) => {
        setFilters(newFilters);
    };

    const handleApplyFilters = () => {
        getTeams(0);
    };

    return (
        <div className="leaguesTeamsPage">
            <div className="title">
                <button className="filled arrow" onClick={() => navigate(-1)}><RiArrowLeftWideLine className="arrow"/>
                </button>
                <h1>{leagueName} {t("teams")}</h1>
            </div>

            { !burgerMenu && (
                <div className="filters-container">
                    <FiltersRenderer model={selectedModel} onFilterChange={handleFiltersChange} sportId={sportId}/>
                    <button onClick={handleApplyFilters}>{t("apply_filters")}</button>
                </div>
            )}

                <SearchBlock
                    cardSizes={globalVariables.cardLayouts}
                    gridSize={gridSize}
                    postsPerPage={teamsPerPage}
                    onGridSizeChange={handleGridSizeChange}
                    pageCount={pageCount}
                    currentPage={currentPage}
                    onPageChange={handlePageClick}
                    loading={loading}
                    paginationKey={paginationKey}
                    handleOpenMenu={handleOpenMenu}
                    menuIcon={menuIcon}
                    setMenuIcon={setMenuIcon}
                    burgerMenu={burgerMenu}
                    menuIsOpen={menuIsOpen}
                    selectedModel={selectedModel}
                    handleFiltersChange={handleFiltersChange}
                    sportId={sportId}
                    count={currentTeams.length}
                    handleApplyFilters={handleApplyFilters}
                    setMenuIsOpen={setMenuIsOpen}

                    children={currentTeams.map((item) => (
                        <TeamCard
                            leagueName={item.team_name}
                            img={item.logo}
                            size={gridSize.baseColumns === 2 ? "small" : gridSize.baseColumns === 5 ? "medium" : "large"}
                            sport={item.sport}
                            id={item.id}
                        />
                    ))}>
                </SearchBlock>
        </div>
    );
}

export default TeamPage;