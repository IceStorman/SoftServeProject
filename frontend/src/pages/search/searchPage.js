import React, { useState, useEffect } from "react";
import FiltersRenderer from "../../components/filters/filterRender";
import useTranslations from "../../translationsContext";
import axios from "axios";
import apiEndpoints from "../../apiEndpoints";
import { toast } from "sonner";
import { TfiLayoutLineSolid } from "react-icons/tfi";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import ReactPaginate from "react-paginate";
import useBurgerMenu from "../../customHooks/useBurgerMenu";
import globalVariables from "../../globalVariables";
import { FaFilter, FaTimes } from "react-icons/fa";
import useBurgerMenuState from "../../customHooks/useBurgerMenuState";
import SearchBlock from "../../components/containers/searchBlock";
import StreamCard from "../../components/cards/streamCard";
import LeagueCard from "../../components/cards/leagueCard";
import TeamCard from "../../components/cards/teamCard";

function SearchPage() {
    const { t } = useTranslations();
    const [selectedModel, setSelectedModel] = useState("streams");
    const [filters, setFilters] = useState([]);
    const [currentItems, setCurrentItems] = useState([]);
    const [pageCount, setPageCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(0);
    const burgerMenu = useBurgerMenu(globalVariables.windowSizeForBurger.streams);
    const [sportId, setSportId] = useState(null);
    const [leagueId, setLeagueId] = useState(null);
    const [inputValue, setInputValue] = useState(""); 
    const [prevInputValue, setPrevInputValue] = useState("");

    const { menuIsOpen, menuIcon, handleOpenMenu, handleCloseMenu } = useBurgerMenuState({
        menuSelector: ".filters-container",
        buttonSelector: ".menu-btn",
        initialIcon: <FaFilter size={28} />, 
        closeIcon: <FaTimes size={28} color="black" />,
    });

    const componentMap = (type, item) => {
        const componentsCard = {
            leagues: <LeagueCard
                    leagueName={item.name}
                    img={item.logo}
                    id={item.id}
                    sportId={sportId}
                    />,
        }
        console.log(componentsCard[type]);
        return componentsCard[type] || {};
    };

    const fetchData = async (model, page = 0) => {
        setPrevInputValue(inputValue);
    
        let filtersData = [...filters];
    
        if (sportId) {
            filtersData.push({ filter_name: "sport_id", filter_value: sportId });
        }
        if (leagueId) {
            filtersData.push({ filter_name: "league_id", filter_value: leagueId });
        }
    
        try {
            const endpointMap = {
                streams: apiEndpoints.stream.getStreamsSearch,
                leagues: apiEndpoints.sports.getLeagueSearch,
                teams: apiEndpoints.teams.getTeamsAll, 
            };
    
            if (!endpointMap[model]) {
                throw new Error(`Unknown model: ${model}`);
            }
    
            const response = await axios.post(
                `${apiEndpoints.url}${endpointMap[model]}`,
                {
                    pagination: { page: page + 1, per_page: 10 },
                    filters: filtersData,
                },
                { headers: { "Content-Type": "application/json" } }
            );
    
            setCurrentItems(response.data.items || []);
            setPageCount(Math.ceil(response.data.count / 10));
            console.log(response.data.items)
        } catch (error) {
            setPageCount(0);
            toast.error(`Error loading ${model}: ${error.message}`);
        }
    };    

    useEffect(() => {
        fetchData(selectedModel, 0);
    }, [selectedModel, filters]);

    return (
        <div className="streams-page">
            <div className="model-selection">
                {["streams", "leagues", "teams"].map((model) => (
                    <button
                        key={model}
                        className={selectedModel === model ? "active" : ""}
                        onClick={() => setSelectedModel(model)}
                    >
                        {model.charAt(0).toUpperCase() + model.slice(1)}
                    </button>
                ))}
            </div>

            {!burgerMenu && (
                <div className={`filters-container ${menuIsOpen ? "show" : ""}`}>
                    <FiltersRenderer model={selectedModel} onFilterChange={setFilters} />
                    <button onClick={() => fetchData(selectedModel, 0)}>{t("apply_filters")}</button>
                </div>
            )}

            {burgerMenu && (
                <div className="filter-wrapper">
                    <button className={"menu-btn"} onClick={handleOpenMenu}>{menuIcon}</button>
                    {menuIsOpen && (
                        <div className="filters-container show">
                            <FiltersRenderer model={selectedModel} onFilterChange={setFilters} />
                            <button onClick={() => fetchData(selectedModel, 0)}>{t("apply_filters")}</button>
                        </div>
                    )}
                </div>
            )}

            <SearchBlock
                gridSize={{ columns: 3, rows: 2, cardSize: { width: 4000, height: 400 } }}
                postsPerPage={10}
                pageCount={pageCount}
                currentPage={currentPage}
                onPageChange={(event) => {
                    setCurrentPage(event.selected);
                    fetchData(selectedModel, event.selected);
                }}
                paginationKey={selectedModel}
                count={currentItems.length}
            
                children={currentItems.length > 0 ? (
                    currentItems.map((item) => {
                       return componentMap(selectedModel, item);
                    })
                ) : (
                    <div>{t("no_results_found")}</div>
                )}
            >
            </SearchBlock>
        </div>
    );
}

export default SearchPage;
