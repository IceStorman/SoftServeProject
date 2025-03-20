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
import FilterImport, {filtersImports} from "../../components/filters/filterImport";
import FiltersRenderer from "../../components/filters/filterRender";

function LeaguePage() {
    const { sportName } = useParams();

    const navigate = useNavigate();

    const location = useLocation();
    const stateData = location.state || {};
    const sportId = stateData.sportId;

    const cardSizes = {
        large: { rows: 4, columns: 4, cardSize: { width: 250, height: 280 }, postsPerPage: 16 },
        medium: { rows: 5, columns: 5, cardSize: { width: 180, height: 210 }, postsPerPage: 25 },
        small: { rows: 10, columns: 2, cardSize: { width: 500, height: 100 }, postsPerPage: 20 }
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

        const initialFiltersData = {
            'filter_name': 'sport_id',
            'filter_value': sportId
        }

        const filtersData = [...filters]
        filtersData.push(initialFiltersData)
        console.log(filtersData)

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
            console.log(response)
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
        console.log("Filters:", newFilters);
    };

    const handleApplyFilters = () => {
        getLeagues(0);
    };


    return (

        <div className="leagues-page">
            <div className="title">
                <button className="filled arrow" onClick={() => navigate(-1)}><RiArrowLeftWideLine className="arrow"/>
                </button>
                <h1>{sportName} {t("leagues")}</h1>
            </div>

            <div className="filters-container">
                <FiltersRenderer model={selectedModel} onFilterChange={handleFiltersChange} sportId={sportId}/>
                <button onClick={handleApplyFilters}>{t("apply_filters")}</button>
            </div>

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
                </SearchBlock> : <NoItems text='No leagues were found'/>}
        </div>
    );
}

export default LeaguePage;