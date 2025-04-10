import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints.js";
import { toast } from "sonner";
import LeagueCard from "../../components/cards/leagueCard"
import { RiArrowLeftWideLine } from "react-icons/ri";
import useTranslations from "../../translationsContext";
import FiltersRenderer from "../../components/filters/filterRender";
import {FaFilter, FaTimes} from "react-icons/fa";
import SearchBlock from "../../components/containers/searchBlock";
import globalVariables from "../../globalVariables";
import useBurgerMenu from "../../customHooks/useBurgerMenu";
import useBurgerMenuState from "../../customHooks/useBurgerMenuState";


function LeaguePage() {
    const { sportName } = useParams();

    const navigate = useNavigate();
    const location = useLocation();
    const stateData = location.state || {};
    const sportId = stateData.sportId;
    const burgerMenu = useBurgerMenu(`${globalVariables.windowSizeForBurger.filters}`);
    const initialIcon = <FaFilter size={28} />;
    const closeIcon = <FaTimes size={28} color="black" />;

    const { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu } = useBurgerMenuState({
        initialIcon: initialIcon,
        closeIcon: closeIcon,
    });

    const calculateColumns = (width, layout) => {
        if (width > globalVariables.windowsSizesForCards.desktopLarge) return layout.baseColumns;
        if (width > globalVariables.windowsSizesForCards.desktopMid) return Math.max(layout.baseColumns - 1, layout.minColumns);
        if (width > globalVariables.windowsSizesForCards.tablet) return Math.max(layout.baseColumns - 2, layout.minColumns);
        if (width > globalVariables.windowsSizesForCards.mobileLarge) {
            return layout.baseColumns === 4
                ? Math.max(layout.baseColumns - 2, layout.minColumns)
                : Math.max(layout.baseColumns - 3, layout.minColumns);
        }
        if (width < globalVariables.windowsSizesForCards.mobileSmall) {
            if (layout.baseColumns === 2) {
                return layout.minColumns - 1;
            }
        }
        return layout.minColumns;
    };

    const [gridSize, setGridSize] = useState({
        ...globalVariables.cardLayouts.large,
        columns: calculateColumns(window.innerWidth, globalVariables.cardLayouts.large)
    });

    const calculateLeaguesPerPage = (layout) => {
        if (layout.minColumns === 1) return layout.alwaysColumns * 2;
        return gridSize.baseRows * gridSize.alwaysColumns
    }

    const [leaguesPerPage, setLeaguesPerPage] = useState(calculateLeaguesPerPage(globalVariables.cardLayouts.large));

    useEffect(() => {
        setLeaguesPerPage(gridSize.baseRows * gridSize.columns);
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

    const [currentLeagues, setCurrentLeagues] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [paginationKey, setPaginationKey] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const [passedPosts, setPassedPosts] = useState(0);
    const { t } = useTranslations();

    useEffect(() => {
        let page = Math.floor(passedPosts / leaguesPerPage);
        setCurrentPage(page);
        getLeagues(page);
    }, [leaguesPerPage]);

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

        const initialFiltersData = {
            'filter_name': 'sport_id',
            'filter_value': sportId
        }

        const filtersData = [...filters]
        filtersData.push(initialFiltersData)

        try {
            const response = await axios.post(
                `${apiEndpoints.url}${apiEndpoints.sports.getLeagueSearch}`,
                {
                    pagination: {
                        page: page + 1,
                        per_page: leaguesPerPage,
                    },
                    filters: filtersData
                },
                {
                    headers: { 'Content-Type': 'application/json' },
                }
            );

            setCurrentLeagues(response.data.items);
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

    const [selectedModel, setSelectedModel] = useState("leagues");
    const [filters, setFilters] = useState([]);

    const handleFiltersChange = (newFilters) => {
        setFilters(newFilters);
    };

    const handleApplyFilters = () => {
        getLeagues(0);
    };


    return (

        <div className="leaguesTeamsPage">
            <div className="title">
                <button className="filled arrow" onClick={() => navigate(-1)}><RiArrowLeftWideLine className="arrow"/>
                </button>
                <h1>{sportName} {t("leagues")}</h1>
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
                    postsPerPage={leaguesPerPage}
                    onGridSizeChange={handleGridSizeChange}
                    pageCount={pageCount}
                    currentPage={currentPage}
                    onPageChange={handlePageClick}
                    loading={loading}
                    paginationKey={paginationKey}
                    burgerMenu={burgerMenu}
                    selectedModel={selectedModel}
                    handleFiltersChange={handleFiltersChange}
                    sportId={sportId}
                    count={currentLeagues.length}
                    handleApplyFilters={handleApplyFilters}
                    children={currentLeagues.map((item) => (
                        <LeagueCard
                            leagueName={item.name}
                            img={item.logo}
                            sportName={sportName}
                            size={gridSize.baseColumns === 2 ? "small" : gridSize.baseColumns === 5 ? "medium" : "large"}
                            id={item.id}
                            sportId={sportId}
                        />
                    ))}>
                </SearchBlock>
        </div>
    );
}

export default LeaguePage;